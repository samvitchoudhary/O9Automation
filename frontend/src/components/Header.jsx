import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Header.css';

function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  // Determine which button to show based on current page
  const isDashboard = location.pathname === '/';

  return (
    <header className="app-header">
      <div className="header-container">
        {/* LEFT: Clickable Logo Section - Links to Dashboard */}
        <Link to="/" className="logo-section" title="Return to Dashboard" aria-label="Return to Dashboard">
          <img 
            src="/Mondelez-Logo.png" 
            alt="Mondelez International" 
            className="mondelez-logo"
            onError={(e) => {
              console.error('Logo failed to load, using fallback');
              e.target.style.display = 'none';
              const fallback = e.target.nextElementSibling;
              if (fallback) {
                fallback.style.display = 'flex';
              }
            }}
          />
          {/* Text fallback - only shown if logo image fails to load */}
          <div className="mondelez-logo-text" style={{ display: 'none' }}>
            <span className="logo-main">Mondelēz</span>
            <span className="logo-sub">International</span>
          </div>
          <div className="app-info">
            <h1 className="app-title">O9 Test Automation</h1>
            <p className="app-subtitle">SUPPLY CHAIN PLATFORM</p>
          </div>
        </Link>

        {/* RIGHT: Show + button ONLY on Dashboard */}
        <div className="nav-actions">
          {isDashboard && (
            <button 
              onClick={() => navigate('/create')}
              className="icon-button"
              title="Create New Test"
              aria-label="Create New Test"
            >
              <span className="icon-plus">+</span>
            </button>
          )}
          {/* NO HOME BUTTON - Logo serves this purpose */}
        </div>
      </div>
    </header>
  );
}

export default Header;
