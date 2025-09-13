import React, { useEffect, useState } from "react";

import {HelpGroups, HelpContentSeed, HelpPagesSeed} from "./HelpMenuData";
import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";

import "../../styles/GlobalStyles.css";
import "../../styles/FormStyles.css";
import "./HelpPageStyles.css";


const HelpPage: React.FC = () => {
    const [selectedGroup, setSelectedGroup] = useState<string>("Pages");

    useEffect(() => {
        const hash = window.location.hash;
        if (hash) {
            const id = hash.replace("#", "");
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }, []);

    return (
        <div className="app-container">
            <NavBar />
            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">Help Center</h2>

                    <div className="help-top-menu">
                        {HelpGroups.map((g) => (
                            <button
                                key={g.title}
                                className={`help-top-button ${selectedGroup === g.title ? "active" : ""}`}
                                onClick={() => setSelectedGroup(g.title)}
                            >
                                {g.title}
                            </button>
                        ))}
                    </div>

                    <div className="help-content-area">
                        {selectedGroup === "Pages" &&
                            HelpPagesSeed.map((t) => (
                                <article key={t.id} className="help-article" id={`page-${t.id}`}>
                                    <h4 className="help-article-title">{t.title}</h4>
                                    <p className="help-article-purpose">{t.purpose}</p>
                                    <ol className="help-steps">
                                        {t.steps.map((s, i) => (
                                            <li key={i}>{s}</li>
                                        ))}
                                    </ol>
                                </article>
                            ))}

                        {selectedGroup === "Activities" &&
                            HelpContentSeed.map((t) => (
                                <article key={t.id} className="help-article" id={t.id}>
                                    <h4 className="help-article-title">{t.title}</h4>
                                    <p className="help-article-purpose">{t.purpose}</p>
                                    <ol className="help-steps">
                                        {t.steps.map((s, i) => (
                                            <li key={i}>{s}</li>
                                        ))}
                                    </ol>
                                </article>
                            ))}
                    </div>
                    <br/><br/>

                    <Footer />
                </div>
            </div>
        </div>
    );
};

export default HelpPage;
