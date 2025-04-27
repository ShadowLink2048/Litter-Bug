// src/pages/GarbagePhotoPage.js
import React, { useState } from 'react';
import { usePage } from '../../PageContext';
import './ThrowawayPhoto.css';

function ThrowawayPhotoPage() {
    const { setCurrentPage } = usePage();
    const [image, setImage] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(true); // Modal opens by default for upload
    const [playerId, setPlayerId] = useState('12345'); // Example player ID, replace with actual logic
    const [points, setPoints] = useState(0); // Points state

    const getPointsFromLocalStorage = () => {
        const points = localStorage.getItem('userPoints');
        return points ? parseInt(points, 10) : 0;
    };

    const handleUploadPhoto = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
                setIsModalOpen(false);
                sendPhotoToServer(file);
            };
            reader.readAsDataURL(file);
        }
    };

    const sendPhotoToServer = async (imageFile) => {
        if (!imageFile) {
            alert('Please upload an image first!');
            return;
        }

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('id', playerId);
        formData.append('points', getPointsFromLocalStorage());

        try {
            const response = await fetch('http://localhost:2001/throwgarbage', {
                method: 'POST',
                body: formData,
            });

            const responseData = await response.json();

            if (responseData) {
                if (!responseData.error) {
                    let points = responseData.points;
                    if (points === 0) {
                        points = 2;
                        alert(
                            `Looks like you forgot to snap a photo picking it up, don't worry, you'll still get a couple points.`
                        );
                    } else {
                        alert(
                            `Thank you for throwing away: ${responseData.brand}, you now have ${points} points! Keep it up!`
                        );
                    }
                    localStorage.setItem('userPoints', points);
                } else {
                    alert(`Error: ${responseData.error}`);
                }
            }

            if (responseData.points !== undefined) {
                setPoints(responseData.points);
            }

            setCurrentPage('walk');
        } catch (error) {
            alert('Error sending photo to the server');
            console.error('Error:', error);
        }
    };

    return (
        <div className="garbage-photo-page">
            {image && (
                <div className="image-container">
                    <img src={image} alt="Uploaded" className="captured-image" />
                </div>
            )}

            <img src="/throwaway.gif" alt="Loading" className="loading-image" />

            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>Please Upload a Photo</h3>
                        <input type="file" accept="image/*" onChange={handleUploadPhoto} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default ThrowawayPhotoPage;