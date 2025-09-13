import React, { useState } from "react";
import { SideMenuData, SidebarItem } from "./SideMenuData";

import "../../components/side_menu/SideMenuStyles.css";



const SideMenu: React.FC = () => {
    const [openSubMenu, setOpenSubMenu] = useState<string | null>(null);

    const handleToggleSubMenu = (title: string) => {
        setOpenSubMenu(openSubMenu === title ? null : title);
    };

    const renderMenuItem = (item: SidebarItem) => {
        const hasSubMenu = item.subMenu && item.subMenu.length > 0;

        return (
            <div
                key={item.title}
                className={`menu-item ${hasSubMenu ? "has-submenu" : ""}`} >
                <a href={item.path} className="menu-item-header" onClick={() => handleToggleSubMenu(item.title)}>
                    <span className="icon">{item.icon}</span>
                    <span className="label">{item.title}</span>
                    <span className="arrow">{item.arrow}</span>
                </a>
                {hasSubMenu && openSubMenu === item.title && (
                    <div className="sub-menu">
                        {item.subMenu?.map((subItem: SidebarItem) => (
                            <a key={subItem.title} href={subItem.path} className="sub-menu-item">
                                <span className="icon">{subItem.icon}</span>
                                <span className="label">{subItem.title}</span>
                            </a>
                        ))}
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="menu-container">
            {SideMenuData.map((item) => renderMenuItem(item))}
        </div>
    );
};

export default SideMenu;
