import React, { useState } from "react";
import { HelpGroups, HelpItem } from "./HelpMenuData";

type Props = {
    onNavigate?: (anchor: string) => void;
};

const HelpMenu: React.FC<Props> = ({ onNavigate }) => {
    const [open, setOpen] = useState<string | null>("Pages");

    const handle = (g: string) => setOpen(open === g ? null : g);

    const clickItem = (it: HelpItem) => {
        if (onNavigate) onNavigate(it.anchor);
        else window.location.hash = it.anchor;
    };

    return (
        <div className="help-menu">
            {HelpGroups.map((g) => (
                <div key={g.title} className="help-menu-group">
                    <button className="help-menu-group-header" onClick={() => handle(g.title)}>
                        <span className="help-menu-group-title">{g.title}</span>
                        <span className={`help-menu-group-arrow ${open === g.title ? "open" : ""}`}>▾</span>
                    </button>
                    {open === g.title && (
                        <div className="help-menu-items">
                            {g.items.map((it) => (
                                <button key={it.id} className="help-menu-item" onClick={() => clickItem(it)}>
                                    {it.title}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default HelpMenu;
