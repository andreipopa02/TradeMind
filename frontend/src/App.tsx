import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';

import LoginPage from './pages/auth_pages/LoginPage';
import RegisterPage from './pages/auth_pages/RegisterPage';
import HomePage from './pages/home_page/HomePage';
import SettingsPage from "./pages/settings_page/SettingsPage";
import AddAccount from "./pages/trading_accounts_pages/add_new_account/AddAccount";
import HelpPage from "./pages/help_page/HelpPage";
import EconomicCalendarPage from "./pages/economic_calendar_pages/EconomicCalendarPage";
import DashboardPage from "./pages/trading_accounts_pages/view_accounts/DashboardPage";
import AccountDashboard from "./pages/trading_accounts_pages/view_accounts/AccountDasboard";
import MyTradesPage from "./pages/statistics/MyTradesPage";
import MyStatisticsPage from "./pages/statistics/MyStatisticsPage";
import MyStatisticDashboardPage from "./pages/statistics/MyStatisticDashboardPage";
import NewStatisticPage from "./pages/statistics/NewStatisticPage";
import BacktestingPage from "./pages/backtesting_pages/BacktestingPage";
import VerifyEmailPage from "./pages/auth_pages/VerifyEmailPage";
import ResetPasswordPage from "./pages/auth_pages/ResetPasswordPage";
import ForgotPasswordPage from "./pages/auth_pages/ForgotPasswordPage";
import CreateStrategyPage from "./pages/backtesting_pages/CreateStrategyPage";
import MyBacktestsPage from "./pages/backtesting_pages/MyBacktestsPage";
import BacktestDetailsPage from "./pages/backtesting_pages/BacktestDetailsPage";


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />

                {/* Auth pages */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/verify-email" element={<VerifyEmailPage />} />
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/reset-password" element={<ResetPasswordPage />} />

                {/* Trading accounts pages*/}
                <Route path="/accounts/add" element={<AddAccount />} />
                <Route path="/accounts/dashboard" element={<DashboardPage />} />
                <Route path="/accounts/dashboard/:account_id" element={<AccountDashboard />} />

                {/* Statistics pages */}
                <Route path="/statistics/my_trades" element={<MyTradesPage />} />
                <Route path="/statistics/my_statistics" element={<MyStatisticsPage/>} />
                <Route path="/statistics/my_statistics/:statisticId" element={<MyStatisticDashboardPage />} />
                <Route path="/statistics/new_statistic" element={<NewStatisticPage />} />

                {/* Backtesting pages */}
                <Route path="/backtesting/new-session" element={<BacktestingPage />} />
                <Route path="/backtesting/custom-strategy" element={<CreateStrategyPage />} />
                <Route path="/backtesting/my_backtests" element={<MyBacktestsPage />} />
                <Route path="/backtesting/my_backtests/:backtestId" element={<BacktestDetailsPage />} />

                {/* Other pages */}
                <Route path="/home" element={<HomePage />} />
                <Route path="/edit-credentials" element={<SettingsPage />} />
                <Route path="/economic-calendar" element={<EconomicCalendarPage />} />
                <Route path="/help" element={<HelpPage />} />
                <Route path="/settings" element={<SettingsPage />} />
            </Routes>
        </Router>
    );
}

export default App;
