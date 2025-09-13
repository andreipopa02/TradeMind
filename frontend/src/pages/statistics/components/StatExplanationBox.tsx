import React from 'react';

import '../styles/StatExplanationBox.css';



interface StatExplanationBoxProps {
    title: string;
    children: React.ReactNode;
}

const StatExplanationBox: React.FC<StatExplanationBoxProps> = ({ title, children }) => {
    return (
        <div className="stat-explanation-box">
            <h3>{title}</h3>
            <p>{children}</p>
        </div>
    );
};

export default StatExplanationBox;
