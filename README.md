# 📊 Retail Sales Performance Dashboard

🔗 **[Live Demo](https://dashboard-bi-hznxc4gxfkg43m93l39myi.streamlit.app)**

Interactive sales analytics dashboard built with Python and Streamlit, featuring cross-filter interactivity across all charts.


## 🎯 Objective

Analyze retail sales performance across products, categories, regions and time periods — identifying trends, top performers and revenue distribution.

---

## ⚙️ Stack

| Tool | Use |
|------|-----|
| Python 3.12 | Core language |
| Pandas 2.2 | Data manipulation |
| Plotly | Interactive charts |
| Streamlit | Dashboard framework |
| OpenPyXL | Excel export |

---

## 📁 Project Structure

```
dashboard_bi/
├── data/
│   ├── superstore.csv          # Raw dataset
│   └── superstore_clean.csv    # Cleaned dataset
├── screenshots/
│   └── overview.png
├── dashboard.py                # Main dashboard
├── data_prep.py                # Data cleaning pipeline
├── requirements.txt
└── README.md
```

---

## 📊 Features

- **4 KPI cards** — Total Sales, Average Ticket, Total Orders, Unique Customers
- **Monthly Sales Evolution** — click a point to cross-filter all charts
- **Top 5 Products by Sales** — horizontal bar chart
- **Sales by Category** — donut chart with percentage breakdown
- **Sales by State** — full US state breakdown
- **Cross-filter** — clicking the timeline or category filters all indicators simultaneously
- **Global filters** — Year, Region, Category via sidebar

---

## 💡 Key Insights

- **Technology** leads revenue with **36.4%** of total sales
- **California, New York and Texas** are the top 3 states by volume
- Sales show a clear **upward trend** from 2014 to 2017
- The **Canon imageCLASS 2200** is the single highest-revenue product

---

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/guilherme-dionysio/dashboard-bi.git
cd dashboard-bi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Prepare data
python data_prep.py

# Run dashboard
streamlit run dashboard.py
```

---

## 📦 Dataset

[Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) — Kaggle  
9,994 records across 4 years (2014–2017), covering US retail sales by product, category, region and customer.

---

*Built by [Guilherme Dionysio](https://github.com/guilherme-dionysio)*