import React from 'react';
import { Link } from 'react-router-dom';
import { BsListCheck, BsGraphUp, BsGraphUpArrow } from "react-icons/bs";
import { AiOutlineAppstore } from "react-icons/ai";
import { FaCalendarAlt, FaCog, FaQuestionCircle } from "react-icons/fa";

import NavBar from '../../components/nav_bar/NavBar';
import SideMenu from '../../components/side_menu/SideMenu';
import Footer from "../../components/footer/Footer";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './HomePageStyles.css';



const HomePage: React.FC = () => {

    const features = [
        {
            title: 'Account tracking',
            desc: 'Centralize all your trading accounts in one place with a clear overview.',
            icon: <BsListCheck />
        },
        {
            title: 'Backtesting',
            desc: 'Test strategies on historical data for objective, repeatable results.',
            icon: <BsGraphUp />
        },
        {
            title: 'Statistics',
            desc: 'Clean metrics for discipline, better decisions, and continuous improvement.',
            icon: <BsGraphUpArrow />
        },
    ];

    const quickLinks = [
        {
            title: 'Add new account',
            desc: 'Quickly create a trading account for tracking.',
            to: '/accounts/add',
            icon: <AiOutlineAppstore /> },
        {
            title: 'Accounts dashboard',
            desc: 'See performance across your accounts.',
            to: '/accounts/dashboard',
            icon: <BsListCheck /> },
        {
            title: 'New backtest session',
            desc: 'Start a new session on market history.',
            to: '/backtesting/new-session',
            icon: <BsGraphUp /> },
        {
            title: 'My backtests',
            desc: 'Review and analyze your previous runs.',
            to: '/backtesting/my_backtests',
            icon: <FaCalendarAlt /> },
        {
            title: 'My statistics',
            desc: 'Monitor your results and reports.',
            to: '/statistics/my_statistics',
            icon: <BsGraphUpArrow /> },
        {
            title: 'Economic calendar',
            desc: 'Macro events that can move the market.',
            to: '/economic-calendar',
            icon: <FaCalendarAlt /> },
        {
            title: 'Settings',
            desc: 'Preferences and platform configuration.',
            to: '/settings',
            icon: <FaCog /> },
        {
            title: 'Help',
            desc: 'FAQs and guides.',
            to: '/help',
            icon: <FaQuestionCircle /> },
    ];

    return (
        <div className="app-container">
            <NavBar />

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">

                    <section className="home-hero">
                        <div className="hero-left">
                            <div className="badge">Built for intraday traders</div>
                            <h1 className="hero-title">Welcome to <span className="brand">TradeMind</span></h1>
                            <p className="hero-subtitle">
                                Organize your trading workflow — from accounts and backtesting to clean, actionable
                                stats.
                                Designed for the market’s pace and fast, informed decisions.
                            </p>
                            <div className="hero-cta">
                                <Link to="/backtesting/new-session" className="btn btn-primary">Start a backtest</Link>
                                <Link to="/accounts/add" className="btn btn-secondary">Add an account</Link>
                            </div>
                        </div>

                        <div className="hero-right">
                            <div className="logo-capsule">
                                <img
                                    src="/trading_icon.png"
                                    alt="TradeMind Logo"
                                    className="logo-image"
                                />

                            </div>
                        </div>

                        <div className="blur-1"/>
                        <div className="blur-2"/>
                    </section>

                    <section className="features">
                        {features.map((f) => (
                            <div key={f.title} className="feature-card">
                                <div className="feature-icon">{f.icon}</div>
                                <div>
                                    <div className="feature-title">{f.title}</div>
                                    <div className="feature-desc">{f.desc}</div>
                                </div>
                            </div>
                        ))}
                    </section>

                    <section className="links">
                        <div className="links-head">
                            <h2 className="links-title">Quick links</h2>
                            <Link to="/help" className="links-more">See full guide</Link>
                        </div>
                        <div className="links-grid">
                            {quickLinks.map((item) => (
                                <div key={item.to} className="link-card">
                                    <div className="link-card-head">
                                        <div className="link-card-icon">{item.icon}</div>
                                        <div>
                                            <div className="link-card-title">{item.title}</div>
                                            <div className="link-card-desc">{item.desc}</div>
                                        </div>
                                    </div>
                                    <div className="link-card-actions">
                                        <Link to={item.to} className="btn btn-secondary w-100">Open</Link>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    <Footer/>
                </div>
            </div>


        </div>
    );
};

export default HomePage;
