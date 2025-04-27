// src/pages/GarbagePhotoPage.js
import React, { useState, useEffect } from 'react';
import { usePage } from '../../PageContext';
import './ThrowawayPhoto.css';

function ThrowawayPhotoPage() {
    const { setCurrentPage } = usePage();
    const [image, setImage] = useState(null);
    const [isCameraAvailable, setIsCameraAvailable] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false); // Modal state
    const [playerId, setPlayerId] = useState('12345'); // Example player ID, replace with actual logic
    const [points, setPoints] = useState(0); // New points state

    const getPointsFromLocalStorage = () => {
        // Get the points from local storage
        const points = localStorage.getItem('userPoints');
    
        // If points exist, return them, else return a default value (0)
        return points ? parseInt(points, 10) : 0;
      };

    useEffect(() => {
        handleCapturePhoto();
    }, []);

    const handleCapturePhoto = async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                video.onloadedmetadata = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    setImage(canvas.toDataURL('image/png'));

                    stream.getTracks().forEach(track => track.stop());
                };
            } catch (err) {
                console.error('Camera not available:', err);
                setIsCameraAvailable(false);
                setIsModalOpen(true);
            }
        } else {
            setIsCameraAvailable(false);
            setIsModalOpen(true);
        }
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
            alert('Please capture or upload an image first!');
            return;
        }

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('id', playerId);
        formData.append('points', getPointsFromLocalStorage()); // Send points to the server

        try {
            const response = await fetch('http://localhost:2001/throwgarbage', {
                method: 'POST',
                body: formData
            });

            const responseData = await response.json();

            if (responseData) {
                // Check if there's not an 'error' key in the responseData
                if (!responseData.error) {
                    // Check if points are zero
                    let points = responseData.points;
                    if (points === 0) {
                        points = 2;  // Set points to 2 if it's 0
                        alert(`Looks like you forgot to snap a photo picking it up, don't worry, you'll still get a couple points.`);
                    } else {
                        alert(`Thank you for throwing away: ${responseData.brand}, you now have ${points} points! Keep it up!`);
                    }

                    // Save the points to local storage
                    localStorage.setItem('userPoints', points);
                }
                else { alert(`Error: ${response.error}`);
            }
            }
            if (responseData.points !== undefined) {
                setPoints(responseData.points); // Update local points based on server response
            }

            setCurrentPage('walk'); // Redirect to 'walk' page after submitting
        } catch (error) {
            alert('Error sending photo to the server');
            console.error('Error:', error);
        }
    };

    return (
        <div className="garbage-photo-page">
            {isCameraAvailable && !image && (
                <div>
                    <button className="camera-button" onClick={handleCapturePhoto}>
                        📸
                    </button>
                </div>
            )}

            {image && (
                <div className="image-container">
                    <img src={image} alt="Captured or Uploaded" className="captured-image" />
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
