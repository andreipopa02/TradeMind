import { AiFillHome, AiOutlineAppstore } from "react-icons/ai";
import {FaCog, FaCalendarAlt} from "react-icons/fa";
import { IoPeople, IoHelpCircle, IoChevronDown } from "react-icons/io5";
import {BsGraphUp, BsGraphUpArrow, BsListCheck} from "react-icons/bs";



export type SidebarItem = {
    title: string;
    path: string;
    icon: React.ReactNode;
    cName?: string;
    subMenu?: SidebarItem[];
    arrow?: React.ReactNode;
};

export const SideMenuData: SidebarItem[] = [
    {
        title: "Home",
        path: "/home",
        icon: <AiFillHome />,
        cName: "side-menu-text",
    },
    {
        title: "Trading Accounts",
        path: "#",
        icon: <IoPeople />,
        cName: "side-menu-text",
        subMenu: [
            {
                title: "Add New Account",
                path: "/accounts/add",
                icon: <AiOutlineAppstore />,
            },
            {
                title: "My Accounts",
                path: "/accounts/dashboard",
                icon: <BsListCheck />,
            },
        ],
        arrow: <IoChevronDown />,
    },
    {
        title: "Backtesting",
        path: "#",
        icon: <BsGraphUp />,
        cName: "side-menu-text",
        subMenu: [
            {
                title: "New Backtesting Session",
                path: "/backtesting/new-session",
                icon: <AiOutlineAppstore />,
            },
            {
                title: "View History of Your Backtestings",
                path: "/backtesting/my_backtests",
                icon: <FaCalendarAlt />,
            },
            {
                title: "Custom Your Personal Strategy",
                path: "/backtesting/custom-strategy",
                icon: <FaCog />,
            },
        ],
        arrow: <IoChevronDown />,
    },
    {
        title: "Statistics",
        path: "#",
        icon: <BsGraphUpArrow />,
        cName: "side-menu-text",
        subMenu: [
            {
                title: "My Trades",
                path: "/statistics/my_trades",
                icon: <BsGraphUp />,
            },
            {
                title: "My Statistics",
                path: "/statistics/my_statistics",
                icon: <BsListCheck />,
            },
            {
                title: "Create New Statistic",
                path: "/statistics/new_statistic",
                icon: <AiOutlineAppstore />,
            },
        ],
        arrow: <IoChevronDown />,
    },
    {
        title: "Economic Calendar",
        path: "/economic-calendar",
        icon: <FaCalendarAlt />,
        cName: "side-menu-text",
    },
    {
        title: "Settings",
        path: "/settings",
        icon: <FaCog />,
        cName: "side-menu-text",
    },
    {
        title: "Help",
        path: "/help",
        icon: <IoHelpCircle />,
        cName: "side-menu-text",
    },
];
