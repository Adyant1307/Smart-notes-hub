     "use client";
     import { useState } from 'react';

     export default function Home() {
       const [search, setSearch] = useState('');
       return (
         <div className="min-h-screen bg-gray-100 p-4">
           <h1 className="text-3xl font-bold mb-4">Smart Notes Hub</h1>
           <input
             type="text"
             placeholder="Search notes/resources..."
             value={search}
             onChange={(e) => setSearch(e.target.value)}
             className="w-full p-2 border rounded mb-4"
           />
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
             {/* Mock notes */}
             <div className="bg-white p-4 rounded shadow">
               <h2>Note Title</h2>
               <p>Tags: #math #notes</p>
               <button className="bg-blue-500 text-white px-4 py-2 rounded">Upvote</button>
             </div>
           </div>
         </div>
       );
     }
     