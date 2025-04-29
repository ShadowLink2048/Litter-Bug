import React, { useState } from 'react';
import { usePage } from '../../PageContext';
import './GarbagePhoto.css';

function GarbagePhotoPage() {
    const { setCurrentPage } = usePage();
    const [image, setImage] = useState();
    const [isModalOpen, setIsModalOpen] = useState();
    const [playerId, setPlayerId] = useState(); 

    const sendPhotoToServer = async (imageFile) => {
        if (!imageFile) {
            alert('Please upload an image first!');
            return;
        }

        // Prepare data to send to the server
        const formData = new FormData();
        formData.image = imageFile;
        formData.id = playerId; 
        
        try {
            const response = await fetch('http://localhost:2434/garbagethrow', {
                methods: 'POST',
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
                <div className="model">
                    <div className="model-content">
                        <h3>Please Upload a Photo</h3>
                        <input type="file" accept="image/*" onChange={handleUploadPhoto} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default GarbagePhotoPage;