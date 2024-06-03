"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { collection, getDocs } from "firebase/firestore";
import { db, storage } from "../firebaseConfig";
import { ref, listAll, getDownloadURL, getMetadata } from "firebase/storage";
import Card from './card'
import "./inventory.css"

const Home = () => {
    const [monuments, setMonuments] = useState([]);
    useEffect(() => {
        const fetchMonuments = async () => {
            const all_monuments = [];
            const querySnapshot = await getDocs(collection(db, "monuments"));
            querySnapshot.forEach((doc) => {
                all_monuments.push(
                    {
                        Name: doc.data().Name,
                        Coordinates: doc.data().Coordinates,
                        Description: doc.data().Description,
                        ImageUrl: "",
                    }
                );
            });
            
            const storageRef = ref(storage, "photos");
            const result = await listAll(storageRef);        

            const photo_data_promises = result.items.map(async (imageRef) => {
                const url = await getDownloadURL(imageRef);
                const metadata = await getMetadata(imageRef);
                const lastDotIndex = metadata.name.lastIndexOf('.');
                const name = lastDotIndex != -1 ? metadata.name.substring(0,lastDotIndex) : metadata.name;
                return {url,name};
            });
            const photoData = await Promise.all(photo_data_promises);
            
            all_monuments.forEach((monument) => {
                const photo = photoData.find((photo) => photo.name == monument.Name);
                if (photo) {
                    monument.ImageUrl = photo.url;
                }
            });

            setMonuments(all_monuments);
        };

        fetchMonuments();

    }, []);

    return (
        <div>
            {/* Navbar */}
            <nav className="bg-gray-800 p-4">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    {/* Left Side (for future use) */}
                    <div className="flex-none">
                        {/* Left side content goes here */}
                    </div>
                    <div className="text-white font-bold text-lg">
                        Monument Information System
                    </div>
                    <div className="flex-none">
                        <ul className="flex space-x-5">
                            <li><Link href="/new-monument" className="text-white text-lg">Add Monument</Link></li>
                            <li><Link href="#" className="text-white text-lg">View in Map</Link></li>
                        </ul>
                    </div>
                </div>
            </nav>

            <div className="max-w-3xl mx-auto mt-4 px-4">
                <input
                    type="text"
                    placeholder="Search..."
                    className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
                />
            </div>
    
            <div className="card-container">
                {monuments.map((monument, index) => 
                    // <Link key={index} to={`/monuments/${monument.Name}`}>
                        <Card key={index} imageUrl={monument.ImageUrl} name={monument.Name} />
                    // </Link>
                )}
            </div>
        </div>
    );   
    
};

export default Home;
