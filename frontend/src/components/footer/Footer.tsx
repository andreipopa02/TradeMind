import React from "react";

import "./FooterStyles.css";



const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="footer-content">

                <div className="footer-column footer-left">
                    <h3 className="footer-logo">TradeMind</h3>
                    <p className="footer-description">
                        All content on this site is provided solely for educational purposes related to trading and does
                        not constitute investment advice, recommendations, or offers to trade any instruments. TradeMind
                        offers simulated trading and educational tools only, is not a broker, and does not accept
                        deposits. Services and data are powered by third-party providers. Access may be restricted where
                        prohibited by law.
                    </p>
                </div>

                <div className="footer-column footer-right">
                    <div className="footer-column-second">
                        <h4>Links</h4>
                        <ul>
                            <li><a href="/home">Home</a></li>
                            <li><a href="/backtesting/new-session">New Backtest Session</a></li>
                            <li><a href="/statistics/my_statistics">Statistics</a></li>
                            <li><a href="/statistics/my_trades">Trades</a></li>
                            <li><a href="/economic-calendar">Economic Calendar</a></li>
                        </ul>
                    </div>

                    <div className="footer-column-second">
                        <h4>Contact</h4>
                        <div className="footer-socials">
                            <a href="mailto:support@trademind.com">support@trademind.com</a>
                            <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
                            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
                        </div>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                <p>&copy; {new Date().getFullYear()} TradeMind. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
