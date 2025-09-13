import React, { useMemo } from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";

import { PerformanceProps } from "../../../types/PerformanceProps";

import "../view_accounts/DashboardStyles.css";
import "./PerformanceChart.css";



ChartJS.register(LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend, Filler);

const PerformanceChart: React.FC<PerformanceProps> = ({ data }) => {
    const css = {
        primary: getComputedStyle(document.body).getPropertyValue("--primary").trim() || "#6cf9e6",
        primary2: getComputedStyle(document.body).getPropertyValue("--primary-2").trim() || "#7aa8ff",
        text: getComputedStyle(document.body).getPropertyValue("--text-color").trim() || "#e8ecf8",
        textSecondary:
            getComputedStyle(document.body).getPropertyValue("--text-color-secondary").trim() || "#a7b0c3",
        border: getComputedStyle(document.body).getPropertyValue("--border").trim() || "rgba(255,255,255,0.14)",
        box: getComputedStyle(document.body).getPropertyValue("--box-color").trim() || "rgba(255,255,255,0.06)",
    };

    const filtered = useMemo(
        () =>
            Array.isArray(data)
                ? data.filter((p, i, arr) => i === 0 || p.balance !== arr[i - 1].balance)
                : [],
        [data]
    );

    const labels = useMemo(
        () => filtered.map((p) => new Date(Number(p.date) * 1000).toLocaleDateString()),
        [filtered]
    );
    const values = useMemo(() => filtered.map((p) => p.balance), [filtered]);

    const chartData = useMemo(() => {
        const backgroundColor = (context: any) => {
            const { ctx, chartArea } = context.chart;
            if (!chartArea) return css.primary2 + "33";
            const g = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            g.addColorStop(0, css.primary2 + "33");
            g.addColorStop(1, css.primary2 + "00");
            return g;
        };
        return {
            labels,
            datasets: [
                {
                    label: "Balance",
                    data: values,
                    borderColor: css.primary,
                    backgroundColor,
                    pointBackgroundColor: css.primary,
                    pointBorderColor: css.primary,
                    pointRadius: 3,
                    pointHoverRadius: 5,
                    borderWidth: 2.5,
                    tension: 0.35,
                    fill: true,
                },
            ],
        };
    }, [labels, values, css]);

    const options: any = useMemo(
        () => ({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false, labels: { color: css.text } },
                title: { display: false },
                tooltip: {
                    enabled: true,
                    backgroundColor: css.box,
                    titleColor: css.text,
                    bodyColor: css.text,
                    borderColor: css.border,
                    borderWidth: 1,
                    callbacks: {
                        label: (ti: any) => `Balance: $${Number(ti.raw).toLocaleString()}`,
                    },
                },
            },
            scales: {
                x: {
                    grid: { color: css.border },
                    ticks: { color: css.textSecondary },
                },
                y: {
                    grid: { color: css.border },
                    ticks: {
                        color: css.textSecondary,
                        callback: (v: any) => `$${Number(v).toLocaleString()}`,
                    },
                },
            },
            elements: { point: { hitRadius: 12 } },
        }),
        [css]
    );

    if (!Array.isArray(data) || data.length === 0) {
        return <p className="chart-empty">No performance data available.</p>;
    }

    return (
        <div className="chart-container">
            <h2 className="chart-title">Performance Chart</h2>

            <div className="chart-canvas-wrap">
                <Line data={chartData} options={options} style={{width: "100%", height: "100%"}}/>
            </div>

        </div>

    );
};

export default PerformanceChart;
