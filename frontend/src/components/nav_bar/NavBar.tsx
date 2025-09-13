import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../ThemeContext';
import { IconContext } from 'react-icons';
import { TokenPayload } from '../../types/TokenPayload';
import * as jwt_decode from "jwt-decode";
import * as FaIcons from 'react-icons/fa';
import * as BiIcons from 'react-icons/bi';
import {FaSun, FaMoon, FaHome} from 'react-icons/fa';

import '../../styles/GlobalStyles.css';
import './NavBar.css';



const NavBar: React.FC = () => {
    const [sidebar, setSidebar] = useState<boolean>(false);
    const [profileMenu, setProfileMenu] = useState<boolean>(false);
    const [userName, setUserName] = useState<string>('');
    const [userEmail, setUserEmail] = useState<string>('');

    const { theme, toggleTheme } = useTheme();

    const toggleSidebar = () => setSidebar(!sidebar);
    const toggleProfileMenu = () => setProfileMenu(!profileMenu);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            const decoded = jwt_decode.jwtDecode<TokenPayload>(token);
            setUserName(`${decoded.first_name} ${decoded.last_name}`);
            setUserEmail(decoded.sub);
        }
    }, []);

    return (
        <>
            <IconContext.Provider value={{ color: 'inherit' }}>
                <div className='navbar'>
                    <div className='menu-bars'>
                        <Link
                            to='/home'
                            onClick={toggleSidebar}
                            aria-label="Home"
                            title="Home"
                        >
                            <FaHome aria-hidden="true" focusable="false"/>
                        </Link>
                    </div>

                    <div className='navbar-icons'>
                        <div className='theme-toggle-icon' onClick={toggleTheme} title="Toggle Theme">
                            {theme === 'dark' ? <FaSun/> : <FaMoon/>}
                        </div>

                        <div className='profile-edit-icon' onClick={toggleProfileMenu}>
                            <BiIcons.BiUserCircle aria-hidden="true" aria-label="profile-icon"/>
                        </div>
                    </div>
                </div>

                <nav className={sidebar ? 'side-menu active' : 'side-menu'}>
                    <div className="menu-close">
                        <FaIcons.FaTimes onClick={toggleSidebar} />
                    </div>
                </nav>

                {profileMenu && (
                    <div className='profile-menu'>
                        <div className='profile-info'>
                            <p><strong>{userName}</strong></p>
                            <p>{userEmail}</p>
                        </div>

                        <div className='profile-actions'>
                            <Link to='/edit-credentials'>
                                <button className='menu-button'>Edit Credentials</button>
                            </Link>
                            <Link to='/login'>
                                <button className='menu-button'>Log Out</button>
                            </Link>
                        </div>
                    </div>
                )}

            </IconContext.Provider>
        </>
    );
};

export default NavBar;
