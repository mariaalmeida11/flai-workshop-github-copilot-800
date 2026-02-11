import React, { useState, useEffect } from 'react';
import { FaDumbbell, FaRunning, FaClock, FaChartLine, FaFire, FaPlay } from 'react-icons/fa';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
      console.log('Fetching workouts from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Workouts data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border text-danger" role="status">
            <span className="visually-hidden">Loading workouts...</span>
          </div>
          <p className="mt-2">Loading workouts...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0"><FaDumbbell className="me-2" /> Workout Suggestions</h2>
        <span className="badge bg-danger rounded-pill">{workouts.length} Workouts</span>
      </div>
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map((workout) => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header bg-gradient">
                  <h5 className="card-title mb-0">{workout.name || workout.title}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text text-muted">{workout.description}</p>
                </div>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong><FaRunning className="me-2" />Type:</strong></span>
                    <span className="badge bg-info">{workout.workout_type || workout.type}</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong><FaClock className="me-2" />Duration:</strong></span>
                    <span className="badge bg-primary">{workout.duration} min</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong><FaChartLine className="me-2" />Difficulty:</strong></span>
                    <span className={`badge ${
                      workout.difficulty === 'Easy' ? 'bg-success' :
                      workout.difficulty === 'Medium' ? 'bg-warning text-dark' :
                      'bg-danger'
                    }`}>
                      {workout.difficulty || 'Medium'}
                    </span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong><FaFire className="me-2" />Calories:</strong></span>
                    <span className="badge bg-success">~{workout.estimated_calories || workout.calories} cal</span>
                  </li>
                </ul>
                <div className="card-footer bg-transparent">
                  <button className="btn btn-sm btn-primary w-100"><FaPlay className="me-2" />Start Workout</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No workout suggestions found
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Workouts;
