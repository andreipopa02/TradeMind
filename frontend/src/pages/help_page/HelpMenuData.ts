import { SideMenuData, SidebarItem } from "../../components/side_menu/SideMenuData";

export type HelpItem = {
    id: string;
    title: string;
    anchor: string;
};

export type HelpGroup = {
    title: "Pages" | "Activities";
    items: HelpItem[];
};

const flattenSideMenu = (items: SidebarItem[], parent?: string): HelpItem[] => {
    const result: HelpItem[] = [];
    items.forEach((it) => {
        if (it.path && it.path !== "#") {
            const id = (parent ? `${parent}-` : "") + it.title.toLowerCase().replace(/\s+/g, "-");
            result.push({
                id,
                title: it.title,
                anchor: `#page-${id}`,
            });
        }
        if (it.subMenu && it.subMenu.length > 0) {
            const base = it.title.toLowerCase().replace(/\s+/g, "-");
            result.push(
                ...flattenSideMenu(
                    it.subMenu,
                    parent ? `${parent}-${base}` : base
                )
            );
        }
    });
    return result;
};

const pageItems: HelpItem[] = flattenSideMenu(SideMenuData);

const activityItems: HelpItem[] = [
    { id: "getting-started-login", title: "Getting Started: Login & Navigation", anchor: "#act-getting-started-login" },
    { id: "manage-accounts", title: "Manage Trading Accounts", anchor: "#act-manage-accounts" },
    { id: "run-backtest", title: "Run a Backtest", anchor: "#act-run-backtest" },
    { id: "analyze-performance", title: "Analyze Performance", anchor: "#act-analyze-performance" },
    { id: "custom-strategy", title: "Build a Custom Strategy", anchor: "#act-custom-strategy" },
    { id: "calendar-alerts", title: "Set Calendar Alerts", anchor: "#act-calendar-alerts" },
    { id: "documents-data", title: "Upload & Organize Documents", anchor: "#act-documents-data" },
    { id: "troubleshooting", title: "Troubleshooting & FAQ", anchor: "#act-troubleshooting" },
];

export const HelpGroups: HelpGroup[] = [
    { title: "Pages", items: pageItems },
    { title: "Activities", items: activityItems },
];

export type HelpTopicContent = {
    id: string;
    title: string;
    purpose: string;
    steps: string[];
    tips?: string[];
    related?: string[];
};


export const HelpPagesSeed = [
    {
        id: "home",
        title: "Home",
        purpose: "The main page that provides quick access to information and navigation to the application's modules.",
        steps: [
            "Open the Home page from the left sidebar.",
            "Review the quick overview of the application.",
            "Navigate to the main modules (Accounts, Backtesting, Statistics, etc.) from the sidebar.",
        ]
    },
    {
        id: "add-account",
        title: "Add New Account",
        purpose: "Add a new demo or real trading account.",
        steps: [
            "Open 'Add New Account' from the sidebar.",
            "Fill in the form with the account details (credentials, broker, account server).",
            "Click the Save button to store the account.",
            "Check 'My Accounts' to confirm the new account is listed."
        ]
    },
    {
        id: "my-accounts",
        title: "My Accounts",
        purpose: "View and manage your saved trading accounts.",
        steps: [
            "Open 'My Accounts' from the sidebar.",
            "Review the list of existing accounts.",
            "Use action buttons (metrix, delete, credentials).",
            "Quickly access statistics for each account."
        ]
    },
    {
        id: "new-backtesting",
        title: "New Backtesting Session",
        purpose: "Run a backtesting session on historical data for a strategy.",
        steps: [
            "Open 'New Backtesting Session' from the sidebar.",
            "Configure the parameters (symbol, time range, timeframe, strategy settings).",
            "Select a strategy from the available list.",
            "Run the backtest and wait for the results to generate."
        ]
    },
    {
        id: "backtesting-history",
        title: "View History of Your Backtestings",
        purpose: "Check the results of your previous backtesting sessions.",
        steps: [
            "Open 'View History of Your Backtestings'.",
            "Select a past session from the list.",
            "Review detailed reports and associated charts.",
            "Compare the performance across different strategies."
        ]
    },
    {
        id: "custom-strategy",
        title: "Custom Your Personal Strategy",
        purpose: "Create or modify your own trading strategies.",
        steps: [
            "Open 'Custom Your Personal Strategy'.",
            "Define the rules and parameters.",
            "Save the strategy.",
            "Test it later in a backtesting session."
        ]
    },
    {
        id: "my-trades",
        title: "My Trades",
        purpose: "Track the history of your executed trades.",
        steps: [
            "Open 'My Trades' from the sidebar.",
            "Review the chronological list of trades.",
            "Use filters to search by date, symbol, or profit.",
            "Add, delete or update a trade."
        ]
    },
    {
        id: "my-statistics",
        title: "My Statistics",
        purpose: "Analyze the performance of your trading accounts.",
        steps: [
            "Open 'My Statistics'.",
            "Select a statistic from the list.",
            "Review charts and key indicators (profit/loss, drawdown, etc.).",
            "Compare performance across multiple symbols."
        ]
    },
    {
        id: "create-statistic",
        title: "Create New Statistic",
        purpose: "Create a custom statistic based on your trades.",
        steps: [
            "Open 'Create New Statistic'.",
            "Select the data source (symbol, period, etc.).",
            "Define the analysis metrics (e.g., volume range, source type, etc.).",
            "Save the statistic and review it in 'My Statistics'."
        ]
    },
    {
        id: "calendar",
        title: "Economic Calendar",
        purpose: "Track important economic events.",
        steps: [
            "Open 'Economic Calendar'.",
            "Review the list of upcoming events.",
            "Filter by country, event type, or impact.",
            "Correlate the information with your trading strategies."
        ]
    },
    {
        id: "settings",
        title: "Settings",
        purpose: "Configure your application preferences and user profile.",
        steps: [
            "Open 'Settings'.",
            "Update your profile information (name, phone, etc.).",
            "Update your password.",
            "Save changes and confirm your account security."
        ]
    },
    {
        id: "help",
        title: "Help",
        purpose: "Access explanations and guidance for the application.",
        steps: [
            "Open 'Help' from the sidebar.",
            "Choose a section from the left menu (Pages / Activities).",
            "Follow the steps explained for the desired page.",
            "Return here anytime for clarifications."
        ]
    }
];



export const HelpContentSeed: HelpTopicContent[] = [
    {
        id: "act-getting-started-login",
        title: "Getting Started: Login & Navigation",
        purpose: "Learn how to sign in and move confidently through the interface.",
        steps: [
            "Open the app and access the Sign In page.",
            "Enter credentials and complete authentication.",
            "Use the left sidebar to access core areas like Trading Accounts, Backtesting, and Statistics.",
            "Use the Help page side menu to jump to any topic."
        ],
        tips: ["Bookmark /home for quick access", "Use keyboard Tab to navigate inputs quickly"],
        related: ["#page-home", "#page-help"]
    },
    {
        id: "act-run-backtest",
        title: "Run a Backtest",
        purpose: "Start a new backtesting session and interpret the results.",
        steps: [
            "Go to Backtesting → New Backtesting Session.",
            "Select market, timeframe, and strategy parameters.",
            "Start the run and wait for results to render.",
            "Open the results screen and review metrics and charts.",
            "Save the session to History to compare later."
        ],
        tips: ["Begin with shorter date ranges to iterate faster", "Save parameter presets you reuse often"],
        related: ["#page-backtesting-new-backtesting-session", "#page-backtesting-view-history-of-your-backtestings"]
    },
    {
        id: "act-analyze-performance",
        title: "Analyze Performance",
        purpose: "Understand how to read key metrics and improve decision-making.",
        steps: [
            "Go to Statistics → My Trades or My Statistics.",
            "Sort and filter by market, date, and profit.",
            "Open a trade to see full details and annotations.",
            "Export a report if needed."
        ],
        tips: ["Create saved filters for intraday sessions", "Compare multiple periods week-over-week"],
        related: ["#page-statistics-my-trades", "#page-statistics-my-statistics"]
    }
];
