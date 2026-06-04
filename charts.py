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
TEXT = "#A4BCC6"  # Enhanced body text brightness

# ── MAXIMIZED SIZING MATRIX FOR HIGH VISIBILITY ────────────────────────────────
FIG_WIDE = (32, 14)    # Massive landscape sizing for single-row items
FIG_TALL = (26, 18)    # Generous scale for complex items like Heatmaps
FIG_SQUARE = (18, 18)  # Maximum breathability for Pie charts

def _base_style():
    """Apply an ultra-clear futuristic dark theme to all charts."""
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": PANEL,
        "axes.edgecolor": GREY,
        "axes.linewidth": 2.5,          # Thicker chart borders
        "axes.labelcolor": TEXT,
        "axes.labelsize": 20,           # Massive axis title text
        "axes.titlesize": 26,           # Massive chart header text
        "axes.titleweight": "bold",
        "xtick.color": TEXT,
        "ytick.color": TEXT,
        "xtick.labelsize": 16,          # Large easily-readable tick markers
        "ytick.labelsize": 16,
        "grid.color": "#1A263F",        # Visible clean grid lines
        "grid.linewidth": 1.2,
        "text.color": TEXT,
        "font.family": "sans-serif",
        "legend.fontsize": 16,          # Big legible legend descriptions
        "legend.title_fontsize": 18,
        "figure.titlesize": 32
    })

def _empty_chart(fig, ax, message):
    """Fallback display with giant text indicator block."""
    ax.clear()
    ax.text(0.5, 0.5, message, color=GOLD, fontsize=24, ha="center", va="center", weight="bold")
    ax.set_axis_off()
    return fig

# ── 1. LINE CHART: Price Trend ────────────────────────────────────────────────
def chart_line(df: pd.DataFrame):
    _base_style()
    if df.empty:
        fig, ax = plt.subplots(figsize=FIG_WIDE)
        return _empty_chart(fig, ax, "No data matching active filter pipeline.")

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    
    # Plotting line with enhanced structural thickness
    ax.plot(df["Date"], df["Price"], color=GOLD, linewidth=4.5, label="Closing Value (USD)", zorder=3)
    
    # Accentuate points if looking at small time horizons
    if len(df) < 60:
        ax.scatter(df["Date"], df["Price"], color=GOLD2, s=120, edgecolors=BG, linewidths=2, zorder=4)

    ax.set_title("Bitcoin Price Evaluation Velocity Over Time", pad=25)
    ax.set_xlabel("Timeline Horizon", labelpad=15)
    ax.set_ylabel("Asset Valuation Price ($ USD)", labelpad=15)
    ax.grid(True, linestyle="--", alpha=0.6)
    
    # Cleaner layout configuration for numbers
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    ax.legend(loc="upper left", framealpha=0.9, facecolor=BG, edgecolor=GREY, borderpad=1.2)
    plt.tight_layout()
    return fig

# ── 2. AREA CHART: Growth Context ─────────────────────────────────────────────
def chart_area(df: pd.DataFrame):
    _base_style()
    if df.empty:
        fig, ax = plt.subplots(figsize=FIG_WIDE)
        return _empty_chart(fig, ax, "No data matching active filter pipeline.")

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    ax.fill_between(df["Date"], df["Price"], color=GOLD, alpha=0.25, zorder=2)
    ax.plot(df["Date"], df["Price"], color=GOLD, linewidth=4.0, zorder=3)

    ax.set_title("Bitcoin Cumulative Asset Valuation Trajectory Landscape", pad=25)
    ax.set_xlabel("Timeline Horizon", labelpad=15)
    ax.set_ylabel("Price Level ($ USD)", labelpad=15)
    ax.grid(True, linestyle=":", alpha=0.5)
    
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    plt.tight_layout()
    return fig

# ── 3. HISTOGRAM: Return Density ──────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame):
    _base_style()
    if df.empty or "Change %" not in df.columns:
        fig, ax = plt.subplots(figsize=FIG_WIDE)
        return _empty_chart(fig, ax, "Data series component is absent.")

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    
    # Draw clear distribution density curve bars
    sns.histplot(
        data=df, x="Change %", kde=True, ax=ax,
        color=GOLD, edgecolor=BG, linewidth=2, alpha=0.65, zorder=3
    )
    
    # Style customization on the underlying line elements
    if ax.lines:
        ax.lines[0].set_color(GOLD2)
        ax.lines[0].set_linewidth(4.5)

    ax.axvline(0, color=RED, linestyle="--", linewidth=3.0, alpha=0.8, label="Zero Returns Baseline")
    ax.set_title("Daily Percentage Return Vector Density Profile", pad=25)
    ax.set_xlabel("Daily Market Return Flux Percentage (%)", labelpad=15)
    ax.set_ylabel("Historical Record Counts Frequency", labelpad=15)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:+.1f}%"))
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", framealpha=0.9, facecolor=BG, edgecolor=GREY, borderpad=1.2)
    
    plt.tight_layout()
    return fig

# ── 4. SCATTER PLOT: Volumetric Intersections ─────────────────────────────────
def chart_scatter(df: pd.DataFrame):
    _base_style()
    if df.empty:
        fig, ax = plt.subplots(figsize=FIG_WIDE)
        return _empty_chart(fig, ax, "No records captured.")

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    
    # Isolate valid data matrices safely
    valid = df.dropna(subset=["Vol.", "Price"])
    if valid.empty:
        return _empty_chart(fig, ax, "Volume metric indicators are unavailable.")

    # High clarity scatter plot markers
    scatter = ax.scatter(
        valid["Vol."], valid["Price"],
        c=valid["Change %"], cmap="plasma",
        s=160, alpha=0.75, edgecolors="#111A2E", linewidths=1.2, zorder=3
    )

    cbar = fig.colorbar(scatter, ax=ax, pad=0.02)
    cbar.set_label("Daily Price Shift Value (%)", color=TEXT, fontsize=16, labelpad=12)
    cbar.ax.tick_params(labelsize=14, colors=TEXT)
    
    ax.set_title("Liquidity Mass (Volume Traded) vs Intra-Day Valuation Spread", pad=25)
    ax.set_xlabel("Capital Trading Volume Volume (Traded Count Asset Unit Shares)", labelpad=15)
    ax.set_ylabel("Asset Spot Settlement Target Price ($ USD)", labelpad=15)
    
    ax.xaxis.set_major_formatter(mticker.EngFormatter())
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    return fig

# ── 5. PIE CHART: Structural Allocation ───────────────────────────────────────
def chart_pie(df: pd.DataFrame):
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_SQUARE, facecolor=BG)
    if df.empty or "Direction" not in df.columns:
        return _empty_chart(fig, ax, "No records to classify structural segmentation.")

    counts = df["Direction"].value_counts()
    if counts.empty:
        return _empty_chart(fig, ax, "No dynamic direction metrics classified.")

    labels = [str(x) for x in counts.index]
    colors = [GREEN if x == "Bullish" else RED for x in labels]

    wedges, texts, autotexts = ax.pie(
        counts, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops={"edgecolor": BG, "linewidth": 4, "antialiased": True},
        textprops={"fontsize": 20, "weight": "bold"}
    )

    # Enhance inner labeling clarity metrics
    for text in texts:
        text.set_color(TEXT)
    for autotext in autotexts:
        autotext.set_color(BG)
        autotext.set_fontsize(22)

    ax.set_title("Market Cycle Direction Structure Allocation", pad=35, fontsize=28)
    plt.tight_layout()
    return fig

# ── 6. BAR CHART: Yearly Comparisons ──────────────────────────────────────────
def chart_bar(df: pd.DataFrame):
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    if df.empty:
        return _empty_chart(fig, ax, "No data available.")

    yearly_avg = df.groupby("Year")["Price"].mean().reset_index()
    
    bars = ax.bar(
        yearly_avg["Year"], yearly_avg["Price"],
        color=GOLD, edgecolor=GOLD2, linewidth=1.5, width=0.65, zorder=3
    )

    ax.set_title("Mean Valuation Level Tiers Sorted by Annual Calendar Blocks", pad=25)
    ax.set_xlabel("Calendar Year Era Block", labelpad=15)
    ax.set_ylabel("Average Historical Valuation Base ($ USD)", labelpad=15)
    
    ax.set_xticks(yearly_avg["Year"])
    ax.set_xticklabels(yearly_avg["Year"], rotation=45)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    return fig

# ── 7. COUNT PLOT: Cycle Quantities ───────────────────────────────────────────
def chart_count(df: pd.DataFrame):
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    if df.empty or "Year" not in df.columns or "Direction" not in df.columns:
        return _empty_chart(fig, ax, "Incomplete parameters for rendering.")

    order = sorted(df["Year"].unique())
    sns.countplot(
        data=df, x="Year", hue="Direction",
        palette={"Bullish": GREEN, "Bearish": RED},
        order=order, ax=ax, edgecolor=BG, linewidth=1.5, zorder=3
    )

    ax.set_title("Calendar Cycle Density Count Quantities (Bullish vs Bearish)", pad=25)
    ax.set_xlabel("Calendar Year Era Block", labelpad=15)
    ax.set_ylabel("Quantified Market Days Count Summary", labelpad=15)
    ax.set_xticklabels(order, rotation=45)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.legend(title="Market Context Profile", loc="upper left", framealpha=0.9, facecolor=BG, edgecolor=GREY, borderpad=1.2)
    
    plt.tight_layout()
    return fig

# ── 8. BOX PLOT: Dispersion Spread ────────────────────────────────────────────
def chart_box(df: pd.DataFrame):
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    if df.empty:
        return _empty_chart(fig, ax, "No records ready.")

    order = sorted(df["Year"].unique())
    
    # Thick-lined high-contrast box configurations
    sns.boxplot(
        data=df, x="Year", y="Price", order=order, ax=ax,
        color=PANEL, linecolor=GOLD, linewidth=2.5,
        flierprops={"markerfacecolor": RED, "markeredgecolor": "none", "markersize": 7},
        boxprops={"facecolor": "#0B1A30", "edgecolor": GOLD}
    )

    ax.set_title("Price Variance Threshold Dispersions Across Historical Benchmarks", pad=25)
    ax.set_xlabel("Calendar Year Era Block", labelpad=15)
    ax.set_ylabel("Asset Price Metrics Bracket ($ USD)", labelpad=15)
    ax.set_xticklabels(order, rotation=45)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(True, linestyle="--", alpha=0.4)
    
    plt.tight_layout()
    return fig

# ── 9. HEATMAP: Variable Matrix Interconnections ──────────────────────────────
def chart_heatmap(df: pd.DataFrame):
    _base_style()
    fig, ax = plt.subplots(figsize=FIG_TALL, facecolor=BG)
    
    numeric_cols = ["Price", "Open", "High", "Low", "Vol.", "Change %"]
    valid_cols = [c for c in numeric_cols if c in df.columns]
    
    if len(valid_cols) < 2:
        return _empty_chart(fig, ax, "Insufficient quantitative asset feature pairs.")

    corr = df[valid_cols].corr()

    # Highly clear matrix display with gigantic labels inside cells
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="mako", ax=ax,
        vmin=-1, vmax=1, square=True, linewidths=3.0, linecolor=BG,
        cbar_kws={"shrink": 0.8, "pad": 0.03},
        annot_kws={"size": 22, "weight": "bold"}
    )

    ax.set_title("Market Performance Variable Cross-Correlation Coefficient Matrix", pad=30)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=18)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=18)
    
    plt.tight_layout()
    return fig

# ── 10. VIOLIN PLOT: Return Profiles ──────────────────────────────────────────
def chart_violin(df: pd.DataFrame):
    _base_style()
    year_counts = df["Year"].value_counts()
    valid_years = sorted(year_counts[year_counts >= 20].index)

    if not valid_years:
        fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
        return _empty_chart(fig, ax, "Insufficient data clusters across year rows to plot structural distribution.")

    sub = df[df["Year"].isin(valid_years)]
    samples = []
    labels = []

    for y in valid_years:
        vals = sub[sub["Year"] == y]["Change %"].dropna().values
        if len(vals) > 0:
            samples.append(vals)
            labels.append(str(y))

    fig, ax = plt.subplots(figsize=FIG_WIDE, facecolor=BG)
    if not samples:
        return _empty_chart(fig, ax, "No metrics to draw.")

    parts = ax.violinplot(samples, positions=range(len(labels)), showmedians=True)

    # Bright, thick, high-visibility styling for violin bodies
    for pc in parts["bodies"]:
        pc.set_facecolor(GOLD)
        pc.set_edgecolor(GOLD2)
        pc.set_alpha(0.65)
        pc.set_linewidth(2.0)

    parts["cmedians"].set_color(GREEN)
    parts["cmedians"].set_linewidth(3.5)
    if "cmins" in parts: parts["cmins"].set_edgecolor(GREY)
    if "cmaxes" in parts: parts["cmaxes"].set_edgecolor(GREY)

    ax.set_title("Annual Historical Percentage Returns Wavefront Profile Distribution", pad=25)
    ax.set_xlabel("Calendar Year Era Block", labelpad=15)
    ax.set_ylabel("Daily Return Vector Flux Percentage Level (%)", labelpad=15)
    
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)
    ax.axhline(0, color=RED, linestyle=":", linewidth=2.5, alpha=0.7)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:+.1f}%"))
    ax.grid(True, linestyle="--", alpha=0.4)
    
    plt.tight_layout()
    return fig
