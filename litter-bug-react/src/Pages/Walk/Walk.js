import React, { useEffect, useState } from 'react';
import { usePage } from '../../PageContext';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import './Walk.css';
import "leaflet/dist/leaflet.css";

function WalkPage() {
  const { setCurrentPage } = usePage();
  const [trashBins, setTrashBins] = useState([]);
  const [trashPickups, setTrashPickups] = useState([]);
  const [location, setLocation] = useState(null);

  useEffect(() => {
    // Retrieve data from local storage for trash bins and pickups
    const savedBins = JSON.parse(localStorage.getItem('trashBins')) || [];
    const savedPickups = JSON.parse(localStorage.getItem('trashPickups')) || [];
    setTrashBins(savedBins);
    setTrashPickups(savedPickups);

    // Get the user's current location
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
      },
      (error) => {
        console.error('Geolocation error: ', error);
      }
    );
  }, []);

  const handleQuitClick = () => {
    setCurrentPage('home');
  };

  const handleCameraClick = async () => {
    try {
      // Access the camera
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  
      // Create a video element to display the camera feed
      const video = document.createElement('video');
      video.srcObject = stream;
      video.play();
  
      // Add the video element to the DOM (you can customize this)
      document.body.appendChild(video);
  
      // Set up a canvas to capture the image from the video
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
  
      // Wait for the video to be ready
      video.onloadedmetadata = () => {
        // Set the canvas size to the video dimensions
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
  
        // Draw the video frame to the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
        // Stop the video stream
        stream.getTracks().forEach(track => track.stop());
  
        // Convert the image to a data URL
        const imageDataUrl = canvas.toDataURL('image/png');
  
        // Now that the photo is taken, show the alert
        alert('Camera button clicked. Photo taken successfully.');
  
        // Optionally, you can handle the imageDataUrl, e.g., display it or send it to a server
        console.log(imageDataUrl);
      };
    } catch (err) {
      alert('Error accessing the camera: ' + err.message);
    }
  };
  

  const handleReportClick = () => {
    if (window.confirm('Do you want to add a trash bin to your location?')) {
      const newBin = {
        lat: location.lat,
        lon: location.lon,
      };
      const updatedBins = [...trashBins, newBin];
      localStorage.setItem('trashBins', JSON.stringify(updatedBins));
      setTrashBins(updatedBins);
      alert('Trash bin added!');
    }
  };

  if (!location) {
    return <div>Loading...</div>;
  }

  return (
    <div className="walk-page">
   
      <MapContainer
        center={[location.lat, location.lon]}
        zoom={32} // Zoom level adjusted for roughly 100-yard radius
        style={{ height: '100vh', width: '100%' }}
        scrollWheelZoom={false} // Disable zooming via scroll
        zoomControl={false} // Disable zoom controls
        dragging={true} // Allow panning
        animate={true} // Smooth transition when moving to the user's location
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {/* Markers for trash bins */}
        {trashBins.map((bin, index) => (
          <Marker key={index} position={[bin.lat, bin.lon]} icon={new L.Icon({ iconUrl: 'green-dot.png', iconSize: [25, 25] })}>
            <Popup>Trash Bin</Popup>
          </Marker>
        ))}

        {/* Markers for trash pickups */}
        {trashPickups.map((pickup, index) => (
          <Marker key={index} position={[pickup.lat, pickup.lon]} icon={new L.Icon({ iconUrl: 'blue-dot.png', iconSize: [25, 25] })}>
            <Popup>Trash Pickup</Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Always visible image in bottom right */}
      <img
        src="your-image-url.jpg"
        alt="Your Image"
        className="walk-image"
      />

      {/* Button to go back to Home */}
      <button className="quit-button" onClick={handleQuitClick}>
        ❌
      </button>

      {/* Camera button */}
      <button className="camera-button" onClick={handleCameraClick}>
        📷
      </button>

      {/* Report button */}
      <button className="report-button" onClick={handleReportClick}>
        Report Trash Bin
      </button>
    </div>
  );
}

export default WalkPage;
