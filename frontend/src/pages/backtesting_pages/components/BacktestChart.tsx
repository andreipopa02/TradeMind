import React, { useEffect, useRef } from "react";
import { ColorType, createChart, CrosshairMode, LineStyle, Time } from "lightweight-charts";
import { Candle, ExecutedTrade } from "../../../types/Backtest";

import "./BacktestChartStyles.css";



interface Props {
    data?: unknown[];
    trades: ExecutedTrade[];
    candles: Candle[];
}

const BacktestChart: React.FC<Props> = ({ data, trades, candles }) => {
    const wrapperRef = useRef<HTMLDivElement>(null);
    const chartHostRef = useRef<HTMLDivElement>(null);
    const tooltipRef = useRef<HTMLDivElement>(null);
    const legendRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!chartHostRef.current) return;

        //  theme
        const root = getComputedStyle(document.documentElement);
        const text = root.getPropertyValue("--text-color").trim() || "#dbe5ef";
        const bg = root.getPropertyValue("--box-color").trim() || "#0e1a24";
        const grid = root.getPropertyValue("--grid")?.trim() || "rgba(200, 215, 230, .08)";
        const border = root.getPropertyValue("--border")?.trim() || "rgba(200, 215, 230, .18)";
        const primary = root.getPropertyValue("--primary").trim() || "#6cf9e6";

        //  data prep
        const preparedCandles = (candles || [])
            .map((c) => ({
                ...c,
                time: Math.floor(Number((c as any).time)),
                open: Number((c as any).open),
                high: Number((c as any).high),
                low: Number((c as any).low),
                close: Number((c as any).close),
            }))
            .sort((a, b) => (a.time as number) - (b.time as number))
            .filter((c, i, arr) => i === 0 || c.time > arr[i - 1].time);

        const preparedTrades = (trades || []).map((t) => {
            const openTs = Math.floor(Number(t.open_timestamp));
            let closeTs = Math.floor(Number(t.close_timestamp));
            if (closeTs <= openTs) closeTs = openTs + 1;
            return { ...t, open_timestamp: openTs, close_timestamp: closeTs };
        });

        //  chart
        const chart = createChart(chartHostRef.current, {
            width: chartHostRef.current.clientWidth,
            height: chartHostRef.current.clientHeight,
            layout: {
                background: { type: ColorType.Solid, color: bg || "#0e1a24" },
                textColor: text,
                fontSize: 12,
                fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto",
            },
            grid: {
                vertLines: { color: grid },
                horzLines: { color: grid },
            },
            rightPriceScale: {
                borderColor: border,
                scaleMargins: { top: 0.06, bottom: 0.1 },
            },
            timeScale: {
                borderColor: border,
                timeVisible: true,
                secondsVisible: false,
            },
            crosshair: {
                mode: CrosshairMode.Normal,
                vertLine: { color: primary, width: 1, style: 0, labelBackgroundColor: primary },
                horzLine: { color: primary, width: 1, style: 0, labelBackgroundColor: primary },
            },
        });

        const candleSeries = chart.addCandlestickSeries({
            upColor: "#2ecc71",
            downColor: "#e74c3c",
            borderUpColor: "#2ecc71",
            borderDownColor: "#e74c3c",
            wickUpColor: "#2ecc71",
            wickDownColor: "#e74c3c",
            priceLineVisible: false,
        });

        candleSeries.setData(
            preparedCandles.map((c) => ({
                time: c.time as Time,
                open: Number(c.open),
                high: Number(c.high),
                low: Number(c.low),
                close: Number(c.close),
            }))
        );

        // trade markers + path lines
        candleSeries.setMarkers(
            preparedTrades.flatMap((t) => {
                const isBuy = t.entry_action === "BUY";
                const entry = {
                    time: t.open_timestamp as Time,
                    position: isBuy ? "belowBar" : "aboveBar",
                    color: isBuy ? "#2ecc71" : "#e74c3c",
                    shape: isBuy ? "arrowUp" : "arrowDown",
                    text: t.entry_action,
                } as const;

                const exit = {
                    time: t.close_timestamp as Time,
                    position: t.exit_action === "SELL" ? "aboveBar" : "belowBar",
                    color: t.profit >= 0 ? "#2ecc71" : "#e74c3c",
                    shape: t.exit_action === "SELL" ? "arrowDown" : "arrowUp",
                    text: `${t.exit_action}  ${t.profit >= 0 ? "+" : ""}${t.profit}`,
                } as const;

                return [entry, exit];
            })
        );

        preparedTrades.forEach((t) => {
            const pathSeries = chart.addLineSeries({
                color: t.profit >= 0 ? "#2ecc71" : "#e74c3c",
                lineWidth: 2,
                lineStyle: LineStyle.Dotted,
                priceLineVisible: false,
                lastValueVisible: false,
                crosshairMarkerVisible: false,
            });
            pathSeries.setData([
                { time: t.open_timestamp as Time, value: t.entry_price },
                { time: t.close_timestamp as Time, value: t.exit_price },
            ]);
        });

        // legend + tooltip
        const tooltip = tooltipRef.current!;
        const legend = legendRef.current!;

        const updateLegend = (bar?: any) => {
            if (!legend) return;
            if (!bar || !bar.open || !bar.close) {
                legend.innerHTML = `<span>OHLC:</span> <b>-</b>`;
                return;
            }
            legend.innerHTML =
                `<span>O:</span> <b>${bar.open}</b>` +
                ` <span>H:</span> <b>${bar.high}</b>` +
                ` <span>L:</span> <b>${bar.low}</b>` +
                ` <span>C:</span> <b>${bar.close}</b>`;
        };

        chart.subscribeCrosshairMove((param) => {
            const point = param.point;
            const price = param.seriesData.get(candleSeries) as any;

            updateLegend(price);

            if (!point || !tooltip || !param.time || !price) {
                tooltip.style.display = "none";
                return;
            }
            tooltip.style.display = "block";
            tooltip.style.left = `${point.x}px`;
            tooltip.style.top = `${point.y}px`;
            tooltip.innerHTML = `C: <b>${price.close}</b>`;
        });


        const ro = new ResizeObserver(() => {
            if (!chartHostRef.current) return;
            chart.applyOptions({
                width: chartHostRef.current.clientWidth,
                height: chartHostRef.current.clientHeight,
            });
        });
        ro.observe(chartHostRef.current);

        return () => {
            ro.disconnect();
            chart.remove();
        };
    }, [candles, trades]);

    return (
        <div ref={wrapperRef} className="tm-chart">
            <div className="tm-chart__legend" ref={legendRef}>OHLC: <b>-</b></div>
            <div className="tm-chart__tooltip" ref={tooltipRef} style={{ display: "none" }} />
            <div ref={chartHostRef} className="tv-lightweight-charts" style={{ width: "100%", height: "100%" }} />
        </div>
    );
};

export default BacktestChart;
