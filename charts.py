"""
charts.py
---------
One function per chart type.
Each function receives a filtered DataFrame and returns a Matplotlib Figure.
Color scheme: Futuristic Bitcoin — deep navy + gold on near-black backgrounds.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend (required for Streamlit)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.lines import Line2D

# ── GLOBAL COLORS ─────────────────────────────────────────────────────────────
BG = "#030810"  # deep space background
PANEL = "#080F1E"  # slightly lighter panel
GOLD = "#F7931A"  # Bitcoin orange-gold
GOLD2 = "#FFD27A"  # lighter gold highlight
RED = "#FF4466"  # bearish red
GREEN = "#00E5A0"  # bullish green
GREY = "#2A3A5A"  # grid / border grey
TEXT = "#8AA0BA"  # body text

# ── Sizing ────────────────────────────────────────────────────────────────────
# Make all graphs bigger by using larger figsize values.
FIG_WIDE = (22, 9)
FIG_TALL = (18, 11)
FIG_SQUARE = (12, 12)


def _base_style():
    """Apply the futuristic Bitcoin dark theme to all charts."""
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GREY,
            "axes.labelcolor": TEXT,
            "xtick.color": TEXT,
            "ytick.color": TEXT,
            "text.color": TEXT,
            "grid.color": "#0D1828",
            "grid.linestyle": "--",
            "grid.linewidth": 0.5,
            "font.family": "monospace",
            "legend.facecolor": PANEL,
            "legend.edgecolor": GREY,
            "legend.fontsize": 9,
        }
    )


def _fmt_price(ax, axis="y"):
    """Format axis ticks as dollar amounts."""
    fmt = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


def _title(ax, text):
    """Consistent chart title style."""
    ax.set_title(
        text,
        color=GOLD,
        fontsize=13,
        fontweight="bold",
        pad=12,
        fontfamily="monospace",
    )


def _style_axes(ax):
    """Add futuristic border glow effect to axes."""
    for spine in ax.spines.values():
        spine.set_edgecolor(GREY)
        spine.set_linewidth(0.8)


def _empty_chart(fig, ax, message):
    """Render a placeholder chart when there is no valid data."""
    _base_style()
    ax.text(
        0.5,
        0.5,
        message,
        color=TEXT,
        fontsize=12,
        ha="center",
        va="center",
        wrap=True,
    )
    ax.set_axis_off()
    fig.tight_layout()
    return fig


# ── 1. LINE CHART — Price Over Time ──────────────────────────────────────────
def chart_line(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    ax.plot(
        df["Date"],
        df["Price"],
        color=GOLD2,
        linewidth=3.0,
        solid_capstyle="round",
        zorder=4,
    )
    ax.fill_between(df["Date"], df["Price"], alpha=0.22, color=GOLD)

    # Highlight ATH point
    if not df.empty:
        ath_idx = df["Price"].idxmax()
        ax.scatter(
            df.loc[ath_idx, "Date"],
            df.loc[ath_idx, "Price"],
            color=GOLD2,
            edgecolor=BG,
            linewidth=0.8,
            s=90,
            zorder=6,
            label=f"ATH ${df['Price'].max():,.0f}",
        )

    _title(ax, "Bitcoin Closing Price Over Time")
    ax.set_xlabel("Date", color=TEXT)
    ax.set_ylabel("Price (USD)", color=TEXT)
    _fmt_price(ax)
    ax.legend(framealpha=0.3)
    ax.grid(True, alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 2. BAR CHART — Average Price by Year ─────────────────────────────────────
def chart_bar(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    yearly = df.groupby("Year")["Price"].mean().reset_index()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)

    # Color bars: brightest = highest year
    norm = (yearly["Price"] - yearly["Price"].min()) / (
        yearly["Price"].max() - yearly["Price"].min() + 1
    )
    colors = [plt.cm.YlOrBr(0.35 + 0.6 * n) for n in norm]

    bars = ax.bar(
        yearly["Year"].astype(str),
        yearly["Price"],
        color=colors,
        edgecolor=BG,
        linewidth=0.5,
    )

    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h * 1.015,
            f"${h/1000:.0f}K",
            ha="center",
            va="bottom",
            fontsize=7,
            color=TEXT,
        )

    _title(ax, "Average Closing Price by Year")
    ax.set_xlabel("Year", color=TEXT)
    ax.set_ylabel("Avg Price (USD)", color=TEXT)
    _fmt_price(ax)
    ax.grid(True, axis="y", alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 3. HISTOGRAM — Distribution of Daily Returns ─────────────────────────────
def chart_histogram(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    ax.hist(df["Change %"], bins=60, color=GOLD, edgecolor=BG, alpha=0.85)
    ax.axvline(0, color=RED, linestyle="--", linewidth=1.3, label="Zero")
    ax.axvline(
        df["Change %"].mean(),
        color=GREEN,
        linestyle="--",
        linewidth=1.3,
        label=f"Mean: {df['Change %'].mean():.2f}%",
    )
    _title(ax, "Distribution of Daily % Change")
    ax.set_xlabel("Daily Change (%)", color=TEXT)
    ax.set_ylabel("Frequency", color=TEXT)
    ax.legend(framealpha=0.3)
    ax.grid(True, axis="y", alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 4. SCATTER PLOT — Volume vs Price ────────────────────────────────────────
def chart_scatter(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    sample = df.dropna(subset=["Vol."]).copy()
    colors = sample["Direction"].map({"Bullish": GREEN, "Bearish": RED})

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    ax.scatter(
        sample["Vol."],
        sample["Price"],
        c=colors,
        alpha=0.35,
        s=10,
    )

    _title(ax, "Volume vs Closing Price")
    ax.set_xlabel("Volume (traded)", color=TEXT)
    ax.set_ylabel("Price (USD)", color=TEXT)
    _fmt_price(ax)

    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=GREEN,
            markersize=7,
            label="Bullish",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=RED,
            markersize=7,
            label="Bearish",
        ),
    ]
    ax.legend(handles=handles, framealpha=0.3)
    ax.grid(True, alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 5. PIE CHART — Bullish vs Bearish Days ───────────────────────────────────
def chart_pie(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    counts = df["Direction"].value_counts()

    fig, ax = plt.subplots(figsize=FIG_SQUARE, facecolor=BG)
    wedge_props = {"edgecolor": BG, "linewidth": 2.5}

    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[GREEN, RED][: len(counts)],
        wedgeprops=wedge_props,
        startangle=140,
        textprops={"color": TEXT, "fontsize": 11, "fontfamily": "monospace"},
    )

    _title(ax, "Bullish vs Bearish Days")
    fig.tight_layout()
    return fig


# ── 6. BOX PLOT — Price Distribution by Year ─────────────────────────────────
def chart_box(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    year_counts = df["Year"].value_counts()
    valid_years = sorted(year_counts[year_counts >= 10].index)

    if not valid_years:
        fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
        return _empty_chart(fig, ax, "No year has enough data to render a box plot.")

    sub = df[df["Year"].isin(valid_years)]
    groups = []
    labels = []

    for y in valid_years:
        prices = sub[sub["Year"] == y]["Price"].dropna().values
        if len(prices) > 0:
            groups.append(prices)
            labels.append(str(y))

    if not groups:
        fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
        return _empty_chart(
            fig,
            ax,
            "No price data available for the selected years.",
        )

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    bp = ax.boxplot(
        groups,
        labels=labels,
        patch_artist=True,
        medianprops={"color": GOLD2, "linewidth": 2},
    )

    for patch in bp["boxes"]:
        patch.set_facecolor("#0D1828")
        patch.set_edgecolor(GOLD)
    for whisker in bp["whiskers"]:
        whisker.set_color(GREY)
    for cap in bp["caps"]:
        cap.set_color(GREY)
    for flier in bp["fliers"]:
        flier.set(marker=".", color=GOLD, alpha=0.3, markersize=3)

    _title(ax, "Price Distribution by Year (Box Plot)")
    ax.set_xlabel("Year", color=TEXT)
    ax.set_ylabel("Price (USD)", color=TEXT)
    _fmt_price(ax)
    ax.grid(True, axis="y", alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 7. HEATMAP — Correlation Matrix ──────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    cols = ["Price", "Open", "High", "Low", "Vol.", "Change %", "DayRange"]
    corr = df[cols].dropna().corr()

    fig, ax = plt.subplots(figsize=FIG_TALL, facecolor=BG)
    sns.heatmap(
        corr,
        ax=ax,
        cmap="YlOrBr",
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor=BG,
        annot_kws={"size": 9, "color": TEXT},
        cbar_kws={"shrink": 0.8},
    )

    _title(ax, "Feature Correlation Heatmap")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


# ── 8. AREA CHART — Cumulative Max Price ─────────────────────────────────────
def chart_area(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    df2 = df.copy()

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    ax.fill_between(
        df2["Date"],
        df2["Price"],
        alpha=0.35,
        color=GOLD,
        label="Closing Price",
    )
    ax.plot(
        df2["Date"],
        df2["Price"],
        color=GOLD,
        linewidth=2.8,
        solid_capstyle="round",
    )

    _title(ax, "Price Over Time (Area Chart)")
    ax.set_xlabel("Date", color=TEXT)
    ax.set_ylabel("Price (USD)", color=TEXT)
    _fmt_price(ax)
    ax.legend(framealpha=0.3)
    ax.grid(True, alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 9. COUNT PLOT — Bullish / Bearish Count by Year ──────────────────────────
def chart_count(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    counts = (
        df.groupby(["Year", "Direction"]).size().reset_index(name="Count")
    )

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    years = sorted(counts["Year"].unique())
    x = np.arange(len(years))
    width = 0.35

    for i, (direction, color) in enumerate(
        [("Bullish", GREEN), ("Bearish", RED)]
    ):
        vals = [
            counts[
                (counts["Year"] == y)
                & (counts["Direction"] == direction)
            ]["Count"].sum()
            for y in years
        ]
        ax.bar(
            x + i * width,
            vals,
            width,
            label=direction,
            color=color,
            edgecolor=BG,
            alpha=0.85,
        )

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels([str(y) for y in years])

    _title(ax, "Bullish vs Bearish Days per Year")
    ax.set_xlabel("Year", color=TEXT)
    ax.set_ylabel("Number of Days", color=TEXT)
    ax.legend(framealpha=0.3)
    ax.grid(True, axis="y", alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── 10. VIOLIN PLOT — Daily % Change by Year ─────────────────────────────────
def chart_violin(df: pd.DataFrame) -> plt.Figure:
    _base_style()
    year_counts = df["Year"].value_counts()
    valid_years = sorted(year_counts[year_counts >= 20].index)

    if not valid_years:
        fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
        return _empty_chart(
            fig, ax, "No year has enough data to render a violin plot."
        )

    sub = df[df["Year"].isin(valid_years)]
    samples = []
    labels = []

    for y in valid_years:
        vals = sub[sub["Year"] == y]["Change %"].dropna().values
        if len(vals) > 0:
            samples.append(vals)
            labels.append(str(y))

    if not samples:
        fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
        return _empty_chart(
            fig,
            ax,
            "No daily change data available for the selected years.",
        )

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    parts = ax.violinplot(samples, positions=range(len(labels)), showmedians=True)

    for pc in parts["bodies"]:
        pc.set_facecolor(GOLD)
        pc.set_edgecolor(GOLD2)
        pc.set_alpha(0.55)

    parts["cmedians"].set_color(GREEN)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.axhline(0, color=RED, linestyle="--", linewidth=0.8, alpha=0.7)

    _title(ax, "Daily % Change Distribution by Year (Violin)")
    ax.set_xlabel("Year", color=TEXT)
    ax.set_ylabel("Daily Change (%)", color=TEXT)
    ax.grid(True, axis="y", alpha=0.4)
    _style_axes(ax)
    fig.tight_layout()
    return fig

