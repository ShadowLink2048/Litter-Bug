import React, { useState } from 'react';
import { usePage } from '../../PageContext';
import './GarbagePhoto.css';

function GarbagePhotoPage() {
    const { setCurrentPage } = usePage();
    const [image, setImage] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(true); // Modal opens by default for upload
    const [playerId, setPlayerId] = useState('12345'); // Example player ID, replace with actual logic

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
            alert('Please upload an image first!');
            return;
        }

        // Prepare data to send to the server
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('id', playerId); // Add player ID (or any other argument you need)

        try {
            const response = await fetch('http://localhost:2001/grabgarbage', {
                method: 'POST',
                body: formData
            });
            const responseData = await response.json();
            
            if (responseData) {
              if (!responseData.error) {
                  let points = responseData.points;
                  if (points === 0) {
                      points = 2;
                  } 
                  
                  if (responseData.garbage)
                  {
                    alert(
                        `Thank you for finding that ${responseData.brand}! Once you find a garbage can you'll be able to redeem it for ${points} points! Keep it up!`
                    );
                  } else {
                    alert(
                      `Oops! Looks like whatever you found can't be thrown away (or used for UFO fuel)`
                    );

                  }
                  
                  
              } else {
                  alert(`Error: ${responseData.error}`);
              }
            }

            setCurrentPage('walk'); // Go back to home after the alert
        } catch (error) {
            alert('Error sending photo to the server');
            console.error('Error:', error);
        }
    };

    return (
        <div className="garbage-photo-page">
            {/* Image preview if available */}
            {image && (
                <div className="image-container">
                    <img src={image} alt="Uploaded" className="captured-image" />
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