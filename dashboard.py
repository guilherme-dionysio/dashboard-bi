"""
dashboard.py — Retail Sales Performance Dashboard
Author: Guilherme Dionysio
Stack: Streamlit + Pandas + Plotly
Cross-filter: clicking any chart filters all others via session_state
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Performance",
    page_icon="📊",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0f1117; color: #e0e0e0; }
.metric-card { background: #1c1f2e; border: 1px solid #2a2d3e; border-radius: 12px; padding: 24px 28px; text-align: center; }
.metric-label { font-size: 13px; color: #8a8fa8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
.metric-value { font-size: 36px; font-weight: 700; color: #ffffff; line-height: 1.1; }
.section-title { font-size: 13px; font-weight: 600; color: #8a8fa8; letter-spacing: 0.1em; text-transform: uppercase; margin: 28px 0 10px 0; }
.active-filter { background: #1c2e22; border: 1px solid #4ade80; border-radius: 8px; padding: 8px 14px; font-size: 12px; color: #4ade80; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(Path("data/superstore_clean.csv"), parse_dates=["order_date"])
    return df

df = load_data()

# ── Session state — cross-filter slots ───────────────────────────────────────
defaults = {
    "cf_category":   None,
    "cf_year_month": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar — global filters (baseline) ──────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Global Filters")
    years      = sorted(df["year"].unique())
    sel_years  = st.multiselect("Year", years, default=years)
    regions    = sorted(df["region"].unique())
    sel_regions = st.multiselect("Region", regions, default=regions)
    cats       = sorted(df["category"].unique())
    sel_cats   = st.multiselect("Category", cats, default=cats)

    st.markdown("---")
    if st.button("🔄 Clear cross-filters"):
        st.session_state.cf_category   = None
        st.session_state.cf_year_month = None

# ── Apply global filters ──────────────────────────────────────────────────────
base = df[
    df["year"].isin(sel_years) &
    df["region"].isin(sel_regions) &
    df["category"].isin(sel_cats)
].copy()

# ── Apply cross-filters on top of global filters ──────────────────────────────
cross = base.copy()
if st.session_state.cf_category:
    cross = cross[cross["category"] == st.session_state.cf_category]
if st.session_state.cf_year_month:
    cross = cross[cross["year_month"] == st.session_state.cf_year_month]

# ── Active filter banner ──────────────────────────────────────────────────────
active = [
    f"Category: {st.session_state.cf_category}"     if st.session_state.cf_category   else None,
    f"Period: {st.session_state.cf_year_month}"     if st.session_state.cf_year_month else None,
]
active = [a for a in active if a]

st.markdown("# 📊 Retail Sales Performance")
if active:
    st.markdown(f'<div class="active-filter">🔍 Active filters: {" · ".join(active)}</div>', unsafe_allow_html=True)
st.markdown("---")

# ── KPIs (react to cross-filters) ────────────────────────────────────────────
total_sales     = cross["sales"].sum()
avg_ticket      = cross["sales"].mean() if len(cross) else 0
total_orders    = cross["order_id"].nunique()
total_customers = cross["customer_id"].nunique()

c1, c2, c3, c4 = st.columns(4)
for col, label, fmt in [
    (c1, "Total Sales",      f"${total_sales:,.2f}"),
    (c2, "Average Ticket",   f"${avg_ticket:,.2f}"),
    (c3, "Total Orders",     f"{total_orders:,}"),
    (c4, "Unique Customers", f"{total_customers:,}"),
]:
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{fmt}</div>
    </div>""", unsafe_allow_html=True)

# ── Monthly Sales Evolution (clickable → filters all) ────────────────────────
st.markdown('<div class="section-title">Monthly Sales Evolution — click a point to filter</div>', unsafe_allow_html=True)

monthly = (
    cross.groupby("year_month")["sales"]
    .sum().reset_index().sort_values("year_month")
)

fig_line = px.line(
    monthly, x="year_month", y="sales",
    labels={"year_month": "Month", "sales": "Sales ($)"},
    color_discrete_sequence=["#6ee7b7"],
)
fig_line.update_layout(
    plot_bgcolor="#1c1f2e", paper_bgcolor="#1c1f2e", font_color="#e0e0e0",
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor="#2a2d3e"),
    margin=dict(l=0, r=0, t=10, b=0),
    hovermode="x unified", clickmode="event+select",
)
fig_line.update_traces(line_width=2.5, mode="lines+markers", marker=dict(size=6))

sel_line = st.plotly_chart(fig_line, use_container_width=True, on_select="rerun", key="line_chart")

if sel_line and sel_line.get("selection", {}).get("points"):
    clicked_ym = sel_line["selection"]["points"][0].get("x")
    if clicked_ym and clicked_ym != st.session_state.cf_year_month:
        st.session_state.cf_year_month = clicked_ym
        st.rerun()
elif sel_line and not sel_line.get("selection", {}).get("points"):
    if st.session_state.cf_year_month:
        st.session_state.cf_year_month = None
        st.rerun()

# ── Row 2: Top 5 Products + Sales by Category ────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="section-title">Top 5 Products by Sales</div>', unsafe_allow_html=True)
    top5 = (
        cross.groupby("product_name")["sales"]
        .sum().nlargest(5).reset_index().sort_values("sales")
    )
    top5["product_short"] = top5["product_name"].str[:38] + "…"

    fig_bar = px.bar(
        top5, x="sales", y="product_short", orientation="h",
        labels={"sales": "Sales ($)", "product_short": ""},
        color_discrete_sequence=["#6ee7b7"],
    )
    fig_bar.update_layout(
        plot_bgcolor="#1c1f2e", paper_bgcolor="#1c1f2e", font_color="#e0e0e0",
        xaxis=dict(showgrid=True, gridcolor="#2a2d3e"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_products")

with col_right:
    st.markdown('<div class="section-title">Sales by Category</div>', unsafe_allow_html=True)
    cat_sales = cross.groupby("category")["sales"].sum().reset_index()

    fig_pie = px.pie(
        cat_sales, names="category", values="sales", hole=0.55,
        color_discrete_sequence=["#6ee7b7", "#fbbf24", "#a78bfa"],
    )
    fig_pie.update_layout(
        plot_bgcolor="#1c1f2e", paper_bgcolor="#1c1f2e", font_color="#e0e0e0",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="v", x=0, y=0.5),
    )
    fig_pie.update_traces(
        textposition="outside",
        textinfo="percent+label",
        rotation=30,
        domain=dict(x=[0.2, 0.9], y=[0.1, 0.9]),
    )

    sel_pie = st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")

# ── Sales by State — visual only ─────────────────────────────────────────────
st.markdown('<div class="section-title">Sales by State</div>', unsafe_allow_html=True)

state_sales = (
    cross.groupby("state")["sales"]
    .sum().reset_index()
    .sort_values("sales", ascending=False)
)

fig_state = px.bar(
    state_sales, x="state", y="sales",
    labels={"state": "State", "sales": "Sales ($)"},
    color_discrete_sequence=["#6ee7b7"],
)
fig_state.update_layout(
    plot_bgcolor="#1c1f2e", paper_bgcolor="#1c1f2e", font_color="#e0e0e0",
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor="#2a2d3e"),
    showlegend=False,
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_state, use_container_width=True, key="state_chart")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8a8fa8; font-size:12px;'>"
    "Retail Sales Performance · Guilherme Dionysio · "
    "<a href='https://github.com/guilherme-dionysio' style='color:#6ee7b7;'>GitHub</a>"
    "</p>",
    unsafe_allow_html=True,
)