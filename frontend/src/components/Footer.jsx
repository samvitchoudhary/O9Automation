import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-left">
          <p className="footer-text">
            © {new Date().getFullYear()} Mondelēz International, Inc. All rights reserved.
          </p>
          <p className="footer-subtext">
            O9 Supply Chain Test Automation Platform
          </p>
        </div>
        
        <div className="footer-right">
          <a href="#" className="footer-link">Privacy Policy</a>
          <a href="#" className="footer-link">Terms of Use</a>
          <a href="#" className="footer-link">Support</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
