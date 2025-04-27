// src/pages/GarbagePhotoPage.js
import React, { useState, useEffect } from 'react';
import { usePage } from '../../PageContext';
import './GarbagePhoto.css';

function GarbagePhotoPage() {
    const { setCurrentPage } = usePage();
    const [image, setImage] = useState(null);
    const [isCameraAvailable, setIsCameraAvailable] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false); // Modal state
    const [playerId, setPlayerId] = useState('12345'); // Example player ID, replace with actual logic

    // This will be called when the component mounts to check for camera
    useEffect(() => {
        handleCapturePhoto();
    }, []);

    // Capture photo from the camera
    const handleCapturePhoto = async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                video.onloadedmetadata = () => {
                    // Create a canvas to capture the frame
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    // Convert the canvas to an image URL
                    setImage(canvas.toDataURL('image/png'));

                    // Stop the video stream
                    stream.getTracks().forEach(track => track.stop());
                };
            } catch (err) {
                console.error('Camera not available:', err);
                setIsCameraAvailable(false); // Camera is not available
                setIsModalOpen(true); // Show the upload modal
            }
        } else {
            setIsCameraAvailable(false); // Browser doesn't support camera
            setIsModalOpen(true); // Show the upload modal
        }
    };

    // Handle photo upload from file input
    const handleUploadPhoto = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result); // Store the uploaded image
                setIsModalOpen(false); // Close the modal
                sendPhotoToServer(file); // Immediately send the uploaded file
            };
            reader.readAsDataURL(file);
        }
    };

    // Send the image to the server (grabbing garbage)
    const sendPhotoToServer = async (imageFile) => {
        if (!imageFile) {
            alert('Please capture or upload an image first!');
            return;
        }

        // Prepare data to send to the server
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('id', playerId); // Add player ID (or any other argument you need)

        try {
            const response = await fetch('http://localhost:2001/grabgarbage', { // Specify full URL with port 2001
                method: 'POST',
                body: formData
            });
            const responseData = await response.json();
            alert(`Server Response: ${JSON.stringify(responseData)}`);
            setCurrentPage('walk'); // Go back to home after the alert
        } catch (error) {
            alert('Error sending photo to the server');
            console.error('Error:', error);
        }
    };

    return (
        <div className="garbage-photo-page">
            
            
            {/* Camera Button */}
            {isCameraAvailable && !image && (
                <div>
                    <button className="camera-button" onClick={handleCapturePhoto}>
                        📸
                    </button>
                </div>
            )}

            {/* Image preview if available */}
            {image && (
                <div className="image-container">
                    <img src={image} alt="Captured or Uploaded" className="captured-image" />
                    
                </div>
            )}

            <img src="/pickup.gif" alt="Loading" className="loading-image" />

            {/* Modal for Uploading a Photo */}
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

export default GarbagePhotoPage;
