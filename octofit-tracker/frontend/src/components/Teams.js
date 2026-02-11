import React, { useState, useEffect } from 'react';
import { FaUsers, FaUserFriends, FaCalendarPlus, FaHashtag } from 'react-icons/fa';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
      console.log('Fetching teams from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Teams data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        setTeams(teamsData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">Loading teams...</span>
          </div>
          <p className="mt-2">Loading teams...</p>
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
        <h2 className="mb-0"><FaUserFriends className="me-2" /> Teams</h2>
        <span className="badge bg-success rounded-pill">{teams.length} Teams</span>
      </div>
      <div className="row">
        {teams.length > 0 ? (
          teams.map((team) => (
            <div key={team.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">
                    <span className="badge bg-primary me-2"><FaHashtag />{team.id}</span>
                    {team.name}
                  </h5>
                  <p className="card-text text-muted">{team.description || 'No description available'}</p>
                </div>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <span><strong><FaUsers className="me-2" />Members:</strong></span>
                    <span className="badge bg-info rounded-pill">{team.member_count || team.members?.length || 0}</span>
                  </li>
                  <li className="list-group-item">
                    <strong><FaCalendarPlus className="me-2" />Created:</strong> {new Date(team.created_at).toLocaleDateString()}
                  </li>
                </ul>
                <div className="card-footer bg-transparent">
                  <button className="btn btn-sm btn-outline-primary w-100">View Details</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No teams found
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Teams;
