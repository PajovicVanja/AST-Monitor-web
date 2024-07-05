// CoachesView.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../../Styles/CoachesView.css'; // Import the CSS file

const CoachesView = ({ token }) => {
    const [cyclists, setCyclists] = useState([]);
    const [cyclistData, setCyclistData] = useState({});
    const fetchInterval = 3000; // Interval in milliseconds to fetch the latest data

    useEffect(() => {
        // Fetch currently training cyclists
        const fetchCyclists = async () => {
            try {
                const response = await axios.get('http://localhost:5000/coach/currently_training', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setCyclists(response.data);
            } catch (error) {
                console.error("There was an error fetching the currently training cyclists!", error);
            }
        };

        fetchCyclists();
        const interval = setInterval(fetchLatestData, fetchInterval);

        return () => clearInterval(interval);
    }, [token]);

    const fetchLatestData = async () => {
        try {
            const response = await axios.get('http://localhost:5000/sensor/api/latest-data');
            const data = response.data;

            setCyclistData(prevData => {
                const prevCyclistData = prevData[data.cyclistID] || {};
                const newSpeed = data.speed !== null ? data.speed : prevCyclistData.speed;

                return {
                    ...prevData,
                    [data.cyclistID]: {
                        ...data,
                        speed: newSpeed
                    }
                };
            });
        } catch (error) {
            console.error("There was an error fetching the latest data!", error);
        }
    };

    return (
        <div className="coaches-view">
            <h2>Cyclists Currently in Training</h2>
            <div className="cyclists-list">
                {cyclists.length > 0 ? (
                    cyclists.map(cyclist => (
                        <div key={cyclist.cyclistID} className="cyclist-card">
                            <h3>{cyclist.name} {cyclist.surname}</h3>
                            <div className="cyclist-data">
                                <p><strong>Heart Rate:</strong> {cyclistData[cyclist.cyclistID]?.heartrate || 'N/A'}</p>
                                <p><strong>Speed:</strong> {cyclistData[cyclist.cyclistID]?.speed || 'N/A'}</p>
                                <p><strong>Distance:</strong> {cyclistData[cyclist.cyclistID]?.distance || 'N/A'}</p>
                                <p><strong>Duration:</strong> {cyclistData[cyclist.cyclistID]?.duration || 'N/A'}</p>
                            </div>
                        </div>
                    ))
                ) : (
                    <p>No cyclists are currently training</p>
                )}
            </div>
        </div>
    );
};

export default CoachesView;
