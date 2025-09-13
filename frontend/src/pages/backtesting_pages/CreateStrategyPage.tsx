import React, { useState, useEffect } from "react";
import Select from "react-select";

import { uiStyles} from "../../components/ThemeContext";
import api from "../../configuration/AxiosConfigurations";
import {useAuth} from "../../configuration/UseAuth";

import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";



const strategyTypes = [
    "SMA_CROSSOVER", "EMA_CROSSOVER", "RSI_OVERBOUGHT_OVERSOLD",
    "BOLLINGER_BANDS", "BREAKOUT", "DONCHIAN_CHANNEL"
];

const CreateStrategyPage: React.FC = () => {
    const user = useAuth();
    const [type, setType] = useState("");
    const [description, setDescription] = useState("");
    const [parameters, setParameters] = useState<any>({});
    const [name, setName] = useState("");
    const [success, setSuccess] = useState("");
    const [error, setError] = useState("");
    const strategyOptions = strategyTypes.map(t => ({ value: t, label: t }));

    useEffect(() => {
        if (!type) return;


        api.get(`/api/trademind/strategies/public/by-type/${type}`)
            .then((res) => {
                setDescription(res.data.description);
                setParameters(res.data.parameters);
            })
            .catch(() => setError("Failed to load strategy template."));
    }, [type]);

    const handleParamChange = (key: string, value: string) => {
        setParameters({ ...parameters, [key]: Number(value) });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        try {
            if (!user?.id) {
                setError("You must be logged in to create a strategy.");
                return;
            }

            await api.post("/api/trademind/strategies/create", {
                name,
                description,
                type,
                parameters,
                is_public: false,
                created_by: user.id
            });

            setSuccess("Strategy created successfully!");
            setName(""); setDescription(""); setType(""); setParameters({});
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to create strategy.");
        }
    };

    return (
        <div className="app-container">
            <NavBar/>

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu/>
                </div>

                <div className="page-content">
                    <h2>Create New Strategy</h2>

                    <form onSubmit={handleSubmit} className="form-container">
                        <label>
                            Type:
                            <Select
                                styles={uiStyles}
                                options={strategyOptions}
                                value={type ? { value: type, label: type } : null}
                                onChange={(opt: any) => setType(opt?.value ?? "")}
                                placeholder="Select Type"
                                menuPortalTarget={document.body}
                                menuPosition="fixed"
                            />
                        </label>
                        <label>
                            Name:
                            <input type="text" value={name} onChange={(e) => setName(e.target.value)} required/>
                        </label>
                        <label>
                            Description:
                            <textarea value={description} onChange={(e) => setDescription(e.target.value)}/>
                        </label>
                        {Object.keys(parameters).length > 0 && (
                            <div>
                                <h4>Parameters</h4>
                                {Object.entries(parameters).map(([key, value]) => (
                                    <label key={key}>
                                        {key}:
                                        <input
                                            type="text"
                                            value={String(value)}
                                            onChange={(e) => handleParamChange(key, e.target.value)}
                                        />
                                    </label>
                                ))}
                            </div>
                        )}
                        <button type="submit" className="form-button">Create Strategy</button>
                    </form>

                    {success && <p className="form-success">{success}</p>}
                    {error && <p className="form-error">{error}</p>}
                </div>
            </div>

        </div>
    );
};

export default CreateStrategyPage;
