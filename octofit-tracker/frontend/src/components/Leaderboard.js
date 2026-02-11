import React, { useState, useEffect } from 'react';
import { FaTrophy, FaMedal, FaAward } from 'react-icons/fa';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
      console.log('Fetching leaderboard from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Leaderboard data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border text-warning" role="status">
            <span className="visually-hidden">Loading leaderboard...</span>
          </div>
          <p className="mt-2">Loading leaderboard...</p>
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
        <h2 className="mb-0"><FaTrophy className="me-2" /> Leaderboard</h2>
        <span className="badge bg-warning text-dark rounded-pill">{leaderboard.length} Competitors</span>
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">User</th>
              <th scope="col">Team</th>
              <th scope="col">Total Points</th>
              <th scope="col">Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => {
                // Define badge colors and icons for top 3
                let rankBadge = 'bg-light text-dark';
                let rankIcon = null;
                
                if (index === 0) {
                  rankBadge = 'bg-warning text-dark';
                  rankIcon = <FaTrophy className="me-1" />;
                } else if (index === 1) {
                  rankBadge = 'bg-secondary text-white';
                  rankIcon = <FaMedal className="me-1" />;
                } else if (index === 2) {
                  rankBadge = 'bg-danger text-white';
                  rankIcon = <FaAward className="me-1" />;
                }
                
                return (
                  <tr key={entry.id || index}>
                    <td>
                      <span className={`badge ${rankBadge} rounded-pill`}>
                        {rankIcon} {index + 1}
                      </span>
                    </td>
                    <td>
                      <strong>{entry.user_name || entry.user || `User ${entry.id || index + 1}`}</strong>
                    </td>
                    <td>{entry.team_name || entry.team || 'N/A'}</td>
                    <td>
                      <span className="badge bg-success rounded-pill fs-6">
                        {entry.total_points || entry.points || 0} pts
                      </span>
                    </td>
                    <td>{entry.activity_count || entry.activities || 0}</td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-muted">No leaderboard data found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
