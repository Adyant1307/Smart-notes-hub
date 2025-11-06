from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import Note
import boto3
from elasticsearch import Elasticsearch

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MinIO setup ---
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin"
)

# --- Elasticsearch setup ---
es = Elasticsearch("http://localhost:9200")

# --- Root route ---
@app.get("/")
def read_root():
    return {"message": "Backend is running"}

# --- Upload Notes ---
@app.post("/upload")
async def upload_note(
    title: str = Form(...),
    tags: str = Form(...),
    file: UploadFile = File(...)
):
    db = SessionLocal()
    try:
        bucket_name = "notes-bucket"
        file_path = f"notes/{file.filename}"

        # Upload to MinIO
        s3.upload_fileobj(file.file, bucket_name, file_path)

        # Save in DB
        note = Note(title=title, tags=tags, file_url=file_path)
        db.add(note)
        db.commit()
        db.refresh(note)

        # Index in Elasticsearch
        es.index(
            index="notes",
            id=note.id,
            body={
                "title": note.title,
                "tags": note.tags,
                "file_url": note.file_url
            }
        )

        return {"message": "Uploaded and indexed", "note_id": note.id}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

# --- Search Notes ---
@app.get("/search")
def search_notes(query: str):
    res = es.search(
        index="notes",
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "tags", "file_url"]
                }
            }
        }
    )
    return res["hits"]["hits"]

# --- Upvote Note ---
@app.post("/upvote/{note_id}")
def upvote_note(note_id: int):
    db = SessionLocal()
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        db.close()
        return {"error": "Note not found"}

    note.upvotes += 1
    db.commit()
    db.close()
    return {"message": "Upvoted successfully", "note_id": note_id, "upvotes": note.upvotes}
