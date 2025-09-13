import React from 'react';

import '../styles/StatBoxWrapper.css';



interface StatBoxWrapperProps {
    title?: string;
    children: React.ReactNode;
}

const StatBoxWrapper: React.FC<StatBoxWrapperProps> = ({ title, children }) => {
    return (
        <div className="stat-box-wrapper">
            {title && <h3 className="stat-box-title">{title}</h3>}
            <div className="stat-box-content">
                {children}
            </div>
        </div>
    );
};

export default StatBoxWrapper;
