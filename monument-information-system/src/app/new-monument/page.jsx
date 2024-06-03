"use client";
import './addMonument.css';
import { useState } from 'react';
import { doc, setDoc } from "firebase/firestore";
import { db, storage } from "../../firebaseConfig";
import { ref, uploadBytes } from "firebase/storage";

const AddMonumentPage = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [coordinates, setCoordinates] = useState('');
  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState('');

  const handleImageChange = (e) => {
    if (e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    try{
      await setDoc(doc(db, "monuments", name), {
        Name: name,
        Coordinates: coordinates,
        Description: description,
      });
      const storageRef = ref(storage, `photos/${name}.jpg`);
      await uploadBytes(storageRef, image);
    } catch (error) {
      console.error("Error uploading data:", error);
    }
    setName('');
    setDescription('');
    setCoordinates('');
    setImage(null);
  
  };
  

  return (
    <div className="max-w-lg mx-auto mt-20 p-6 bg-white shadow-md rounded-md">
      <h1 className="text-2xl font-semibold mb-6">Add Monument</h1>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Coordinates:</label>
        <input
          type="text"
          value={coordinates}
          onChange={(e) => setCoordinates(e.target.value)}
          className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Image:</label>
        <input
          type="file"
          onChange={handleImageChange}
          className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
        />
      </div>
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
      >
        Upload
      </button>
      {/* {imageUrl && (
        <div className="mt-4">
          <img src={imageUrl} alt="Uploaded Monument" className="w-full rounded-md" />
        </div>
      )} */}
    </div>
  );
};

export default AddMonumentPage;
