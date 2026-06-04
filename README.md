# ₿ Bitcoin History Dashboard

A professional data visualization dashboard for the Bitcoin History dataset, built for the **Exploratory Data Analysis** course.

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── Bitcoin_History.csv      ← Dataset (exact filename, do NOT rename)
├── notebooks/
│   └── analysis.ipynb           ← EDA notebook (optional exploration)
├── app.py                       ← Main Streamlit dashboard
├── charts.py                    ← All 10 chart functions
├── filters.py                   ← Data loading, cleaning, filter logic
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

---

## ⚙️ How to Install & Run

**Step 1 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2 — Run the dashboard**
```bash
streamlit run app.py
```

**Step 3 — Open in browser**  
Streamlit will automatically open `http://localhost:8501`

---

## 📊 Charts Included

| # | Chart Type   | What it Shows                          |
|---|--------------|----------------------------------------|
| 1 | Line Chart   | Bitcoin closing price over time        |
| 2 | Bar Chart    | Average price per year                 |
| 3 | Histogram    | Distribution of daily % change         |
| 4 | Scatter Plot | Volume vs closing price                |
| 5 | Pie Chart    | Bullish vs Bearish day ratio           |
| 6 | Box Plot     | Price spread / outliers per year       |
| 7 | Heatmap      | Correlation between all features       |
| 8 | Area Chart   | Price vs all-time high trend           |
| 9 | Count Plot   | Bullish/bearish counts per year        |
|10 | Violin Plot  | Daily % change distribution per year  |

---

## 🎛️ Filters (all charts update simultaneously)

- **Date Range** — Slider to pick start/end date
- **Price Range** — Numerical slider for min/max price
- **Year Selector** — Multi-select specific years
- **Market Direction** — Filter for Bullish / Bearish days
- **Keyword Search** — Type a year or month name to search
- **Reset Button** — Clears all filters to default

---

## 💡 Key Insights

1. **Exponential growth** — Bitcoin's price grew from ~$0.10 in 2010 to ~$47,000 in 2024.
2. **High volatility** — Daily % changes follow a near-normal distribution centered around 0%, with heavy tails.
3. **Volume and price** — Higher trading volumes correlate with higher price periods (2017, 2021).
4. **Bullish bias** — Roughly 53–55% of all trading days are bullish (positive return).
5. **2022 bear market** — Visible as a dramatic drop in the area and line charts.
6. **Price–High correlation = 0.99+** — Closing price and daily high are nearly identical (expected).

---

## 🛠️ Tech Stack

| Tool       | Purpose                        |
|------------|--------------------------------|
| Python 3.x | Core language                  |
| Pandas     | Data loading, cleaning, filtering |
| NumPy      | Numerical operations           |
| Matplotlib | Core chart creation            |
| Seaborn    | Heatmap & statistical styling  |
| Streamlit  | Interactive frontend dashboard |

---

*Submission Date: 05-June-2026 | Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi*
