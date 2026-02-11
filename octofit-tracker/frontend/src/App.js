import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import { FaUsers, FaUserFriends, FaRunning, FaDumbbell, FaTrophy, FaDumbbell as FaFitness, FaChartLine, FaPlay } from 'react-icons/fa';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img 
                src="/octofitapp-small.png" 
                alt="OctoFit Logo" 
                className="navbar-logo"
              />
              OctoFit Tracker
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} 
                    to="/users"
                  >
                    <FaUsers className="me-1" /> Users
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} 
                    to="/teams"
                  >
                    <FaUserFriends className="me-1" /> Teams
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} 
                    to="/activities"
                  >
                    <FaRunning className="me-1" /> Activities
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} 
                    to="/workouts"
                  >
                    <FaDumbbell className="me-1" /> Workouts
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} 
                    to="/leaderboard"
                  >
                    <FaTrophy className="me-1" /> Leaderboard
                  </NavLink>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron text-center mb-5">
        <h1 className="display-3 fw-bold"><FaFitness className="me-3" />Welcome to OctoFit Tracker!</h1>
        <p className="lead fs-4 mt-3">Track your fitness activities, compete with your team, and achieve your goals!</p>
        <hr className="my-4" />
        <p className="fs-5">Use the navigation menu above to explore different sections of the app.</p>
        <div className="mt-4">
          <Link to="/activities" className="btn btn-primary btn-lg me-2"><FaPlay className="me-2" />Get Started</Link>
          <Link to="/leaderboard" className="btn btn-outline-light btn-lg"><FaTrophy className="me-2" />View Leaderboard</Link>
        </div>
      </div>

      <div className="row g-4 mt-4">
        <div className="col-md-6 col-lg-4">
          <Link to="/users" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <div className="display-4 mb-3"><FaUsers /></div>
                <h5 className="card-title fw-bold">Users</h5>
                <p className="card-text text-muted">View all registered users and their profiles.</p>
                <span className="btn btn-sm btn-outline-primary mt-2">Explore Users →</span>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6 col-lg-4">
          <Link to="/teams" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <div className="display-4 mb-3"><FaUserFriends /></div>
                <h5 className="card-title fw-bold">Teams</h5>
                <p className="card-text text-muted">Explore teams and their members.</p>
                <span className="btn btn-sm btn-outline-success mt-2">Browse Teams →</span>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6 col-lg-4">
          <Link to="/activities" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <div className="display-4 mb-3"><FaRunning /></div>
                <h5 className="card-title fw-bold">Activities</h5>
                <p className="card-text text-muted">Track all fitness activities and achievements.</p>
                <span className="btn btn-sm btn-outline-info mt-2">View Activities →</span>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6 col-lg-4">
          <Link to="/workouts" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <div className="display-4 mb-3"><FaDumbbell /></div>
                <h5 className="card-title fw-bold">Workouts</h5>
                <p className="card-text text-muted">Get personalized workout suggestions.</p>
                <span className="btn btn-sm btn-outline-danger mt-2">See Workouts →</span>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6 col-lg-4">
          <Link to="/leaderboard" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <div className="display-4 mb-3"><FaTrophy /></div>
                <h5 className="card-title fw-bold">Leaderboard</h5>
                <p className="card-text text-muted">See who's leading the fitness challenge!</p>
                <span className="btn btn-sm btn-outline-warning mt-2">Check Rankings →</span>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6 col-lg-4">
          <div className="card h-100 text-center bg-light">
            <div className="card-body">
              <div className="display-4 mb-3"><FaChartLine /></div>
              <h5 className="card-title fw-bold">Statistics</h5>
              <p className="card-text text-muted">Coming soon: View your fitness statistics and progress.</p>
              <span className="btn btn-sm btn-secondary mt-2 disabled">Coming Soon</span>
            </div>
          </div>
        </div>
      </div>

      <div className="row mt-5 mb-5">
        <div className="col-12">
          <div className="card bg-gradient">
            <div className="card-body text-center py-4">
              <h3 className="fw-bold">Ready to Start Your Fitness Journey?</h3>
              <p className="lead mb-3">Join teams, log activities, and compete with friends!</p>
              <Link to="/activities" className="btn btn-primary btn-lg"><FaPlay className="me-2" />Start Tracking</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
