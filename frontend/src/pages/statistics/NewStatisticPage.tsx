import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from "react-select";
import { uiStyles } from "../../components/ThemeContext";

import api from "../../configuration/AxiosConfigurations";
import {useAuth} from "../../configuration/UseAuth";
import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";

import './styles/NewStatistic.css';



type Session = "Asia" | "London" | "NewYork";

interface NewStatParams {
    session?: Session[];
    source_type?: string;
    market?: string[];
    min_volume?: number;
    max_volume?: number;
    start_date?: string;
    end_date?: string;
}

const NewStatisticPage: React.FC = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [params, setParams] = useState<NewStatParams>({});
    const user = useAuth();
    const typeOptions = [
        { value: "user", label: "USER" },
        { value: "backtest", label: "BACKTEST" }
    ];
    const sessionOptions = [
        { value: "Asia", label: "Asia" },
        { value: "London", label: "London" },
        { value: "NewYork", label: "NewYork" }
    ];

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!user?.id) {
            alert("You must be logged in to create a statistic.");
            return;
        }

        const payload = {
            user_id: user.id,
            name,
            params
        };

        try {
            const res = await api.post("/api/trademind/statistics/create", payload);
            if (res.status === 200 || res.status === 201) {
                navigate("/statistics/my_statistics");
            }
        } catch (err: any) {
            console.error("Error creating statistic:", err);
            alert("Error: " + (err.response?.data?.detail || "Failed to create statistic."));
        }
    };

    return (
        <div className="app-container">
            <NavBar />

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">Create New Statistic</h2>

                    <form onSubmit={handleSubmit} className="form-container">
                        <label>Statistic Name:
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </label>

                        <label>Markets (comma-separated):
                            <input
                                type="text"
                                onChange={(e) => setParams({
                                    ...params,
                                    market: e.target.value.split(',').map(m => m.trim())
                                })}
                                placeholder="e.g., DE30EUR, NAS100USD"
                            />
                        </label>

                        <label>Sessions:
                            <Select
                                styles={{
                                    ...uiStyles,
                                    menuList: (base) => ({
                                        ...base,
                                        maxHeight: "none"
                                    }),
                                }}
                                options={sessionOptions}
                                isMulti
                                closeMenuOnSelect={false}
                                value={(params.session ?? []).map((s: any) => ({value: s, label: s}))}
                                onChange={(opts) =>
                                    setParams({
                                        ...params,
                                        session: opts ? opts.map((o) => o.value) : []
                                    })
                                }
                                placeholder="Select sessions..."
                            />
                        </label>

                        <label>Source Type:
                            <Select
                                styles={uiStyles}
                                options={typeOptions}
                                placeholder="-- select source --"
                                onChange={(opt) => setParams({...params, source_type: opt?.value})}
                            />
                        </label>

                        <label>Volume Range:
                            <div className="volume-range">
                                <input
                                    type="number"
                                    placeholder="Min"
                                    onChange={(e) =>
                                        setParams({
                                            ...params,
                                            min_volume: e.target.value === "" ? undefined : Number(e.target.value),
                                        })
                                    }
                                />
                                <input
                                    type="number"
                                    placeholder="Max"
                                    onChange={(e) =>
                                        setParams({
                                            ...params,
                                            max_volume: e.target.value === "" ? undefined : Number(e.target.value),
                                        })
                                    }
                                />
                            </div>
                        </label>

                        <label>Start Date:
                            <input
                                type="date"
                                onChange={(e) => setParams({...params, start_date: e.target.value})}
                            />
                        </label>

                        <label>End Date:
                            <input
                                type="date"
                                onChange={(e) => setParams({...params, end_date: e.target.value})}
                            />
                        </label>

                        <button
                            type="submit" className="form-button ">Save Statistic
                        </button>
                    </form>

                    <Footer/>

                </div>
            </div>
        </div>
    );
};

export default NewStatisticPage;
