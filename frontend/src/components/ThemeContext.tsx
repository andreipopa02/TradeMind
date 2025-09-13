import React, { createContext, useState, useContext, useEffect } from 'react';
import {calendars, countries} from "./utils";



type Theme = 'light' | 'dark';

interface ThemeContextType {
    theme: Theme;
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
    theme: 'dark',
    toggleTheme: () => {}
});

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [theme, setTheme] = useState<Theme>(() => {
        return (localStorage.getItem('theme') as Theme) || 'dark';
    });

    useEffect(() => {
        document.body.className = theme;
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};





export type SelectOption<T extends string = string> = { value: T; label: T };



export const uiStyles = {
    control: (base:any) => ({
        ...base,
        color: "var(--text-color)",
        backgroundColor: "var(--box-color-alt)",
        borderColor: "var(--border)",
        boxShadow: "none",
        borderRadius: "var(--radius)",
        minHeight: 42,
        ":hover": { borderColor: "var(--primary)" },
    }),
    menuPortal: (base:any) => ({ ...base, zIndex: 9999 }),
    menu: (base:any) => ({
        ...base,
        color: "var(--text-color)",
        backgroundColor: "var(--bg-color)",
        border: "1px solid var(--ring)",
        boxShadow: "var(--shadow)",
        backdropFilter: "blur(20px)",
    }),
    option: (base:any, { isFocused, isSelected }: any) => ({
        ...base,
        backgroundColor: isSelected
            ? "color-mix(in srgb, var(--primary) 22%, transparent)"
            : isFocused
                ? "color-mix(in srgb, var(--primary-2) 14%, transparent)"
                : "transparent",
        color: "var(--text-color)",
        cursor: "pointer",
    }),
    singleValue: (base:any) => ({ ...base, color: "var(--text-color)" }),
    placeholder: (base:any) => ({ ...base, color: "var(--text-color-secondary)" }),
    input: (base:any) => ({ ...base, color: "var(--text-color)" }),
};

export const ui2Styles = {
    control: (base: any, state: any) => ({
        ...base,
        minHeight: 44,
        height: 44,
        borderRadius: "var(--radius)",
        backgroundColor: "var(--box-color-alt)",
        borderColor: state.isFocused ? "var(--primary)" : "var(--border)",
        boxShadow: state.isFocused
            ? "0 0 0 3px color-mix(in srgb, var(--primary) 28%, transparent)"
            : "none",
        transition: "border-color var(--trans), box-shadow var(--trans)",
        ":hover": { borderColor: "var(--primary)" },
        cursor: "pointer",
    }),

    valueContainer: (base: any) => ({
        ...base,
        padding: "0 12px",
        gap: 6,
    }),

    indicatorsContainer: (base: any) => ({
        ...base,
        paddingRight: 8,
        gap: 4,
    }),

    indicatorSeparator: () => ({ display: "none" }),

    dropdownIndicator: (base: any, { isFocused }: any) => ({
        ...base,
        transform: isFocused ? "rotate(180deg)" : "none",
        transition: "transform var(--trans)",
        color: "var(--text-color-secondary)",
        ":hover": { color: "var(--primary)" },
    }),

    singleValue: (base: any) => ({ ...base, color: "var(--text-color)" }),
    placeholder: (base: any) => ({ ...base, color: "var(--text-color-secondary)" }),
    input: (base: any) => ({ ...base, color: "var(--text-color)" }),

    menuPortal: (base: any) => ({ ...base, zIndex: 100000 }),
    menu: (base: any) => ({
        ...base,
        marginTop: 6,
        borderRadius: "var(--radius-xl)",
        backgroundColor: "color-mix(in srgb, var(--box-color) 90%, transparent)",
        border: "1px solid var(--ring)",
        boxShadow: "0 18px 50px rgba(10,20,60,.35)",
        overflow: "hidden",
        backdropFilter: "saturate(120%) blur(10px)",
    }),

    menuList: (base: any) => ({
        ...base,
        padding: 6,
        maxHeight: 260,
    }),

    groupHeading: (base: any) => ({
        ...base,
        color: "var(--text-color-secondary)",
        fontWeight: 800,
        fontSize: 11,
        letterSpacing: ".5px",
        textTransform: "uppercase",
        padding: "6px 10px",
    }),

    option: (base: any, { isFocused, isSelected }: any) => ({
        ...base,
        padding: "10px 12px",
        borderRadius: "10px",
        backgroundColor: isSelected
            ? "color-mix(in srgb, var(--primary) 24%, transparent)"
            : isFocused
                ? "color-mix(in srgb, var(--primary-2) 16%, transparent)"
                : "transparent",
        color: "var(--text-color)",
        cursor: "pointer",
    }),
};


export const calendarOptions: SelectOption<keyof typeof calendars>[] =
    (Object.keys(calendars) as Array<keyof typeof calendars>).map((k) => ({
        value: k,
        label: k,
    }));

export const countryOptions = countries.map(c => ({ value: c, label: c }));

export const genderOptions = ["Male","Female","Other"].map(g => ({ value: g, label: g }));
