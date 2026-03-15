import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from databricks import sql

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hospitality Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
      background-color: #f8f7f4;
  }

  /* ── Hero header ── */
  .hero {
      background: linear-gradient(120deg, #1b3a4b 0%, #2d6a8a 60%, #3a8fa8 100%);
      border-radius: 16px;
      padding: 2.4rem 2.8rem 2rem;
      margin-bottom: 1.6rem;
      color: white;
  }
  .hero-title {
      font-family: 'Playfair Display', serif;
      font-size: 3rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin: 0 0 6px 0;
      line-height: 1.1;
  }
  .hero-subtitle {
      font-size: 0.95rem;
      color: rgba(255,255,255,0.72);
      font-weight: 300;
      margin: 0;
      letter-spacing: 0.3px;
  }
  .hero-badge {
      display: inline-block;
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 20px;
      padding: 3px 12px;
      font-size: 0.78rem;
      margin-right: 8px;
      margin-top: 12px;
  }

  /* ── Metric cards ── */
  div[data-testid="stMetric"] {
      background: white;
      border: 1px solid #e8e4de;
      border-radius: 12px;
      padding: 1.1rem 1.3rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }
  div[data-testid="stMetric"] label {
      font-size: 0.7rem !important;
      text-transform: uppercase;
      letter-spacing: 1.3px;
      color: #888 !important;
      font-weight: 500 !important;
  }
  div[data-testid="stMetricValue"] > div {
      font-family: 'Playfair Display', serif !important;
      font-size: 1.75rem !important;
      color: #1b3a4b !important;
  }

  /* ── Insight box ── */
  .insight-box {
      background: white;
      border: 1px solid #e8e4de;
      border-left: 4px solid #2d6a8a;
      border-radius: 10px;
      padding: 1.4rem 1.6rem;
      line-height: 1.8;
      color: #2c2c2c;
      font-size: 0.94rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }

  /* ── Section dividers ── */
  .section-label {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: #999;
      font-weight: 600;
      margin-top: 2rem;
      margin-bottom: 0.2rem;
  }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
      background-color: #1b3a4b;
  }
  section[data-testid="stSidebar"] * {
      color: rgba(255,255,255,0.85) !important;
  }
  section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
      background-color: #2d6a8a !important;
  }

  /* ── General ── */
  .stApp {
      background-color: #f8f7f4;
  }
</style>
""", unsafe_allow_html=True)


# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    connection = sql.connect(
        server_hostname=st.secrets["DATABRICKS_HOST"],
        http_path=st.secrets["DATABRICKS_HTTP_PATH"],
        access_token=st.secrets["DATABRICKS_TOKEN"],
    )
    df = pd.read_sql("SELECT * FROM hospitality_dev.gold_daily_hotel_metrics", connection)
    connection.close()
    df["arrival_date"] = pd.to_datetime(df["arrival_date"])
    return df


# ── AI Insights ────────────────────────────────────────────────────────────────
def build_insights_prompt(df: pd.DataFrame) -> str:
    top_hotel = df.groupby("hotel")["realized_booking_value"].sum().idxmax()
    worst_cancel = df.groupby("hotel")["cancellation_rate_pct"].mean().idxmax()
    peak_date = df.groupby("arrival_date")["total_bookings"].sum().idxmax().strftime("%B %d, %Y")
    avg_adr = round(df["average_adr"].mean(), 2)
    total_rev = int(df["realized_booking_value"].sum())
    cancel_avg = round(df["cancellation_rate_pct"].mean(), 2)

    return f"""You are a hospitality analytics expert. Based on this hotel booking data summary, write 3-4 concise, actionable insights for a hotel operations manager.

Key metrics:
- Top revenue hotel: {top_hotel}
- Highest cancellation rate hotel: {worst_cancel}
- Peak booking date: {peak_date}
- Average ADR across portfolio: ${avg_adr}
- Total realized revenue: ${total_rev:,}
- Average cancellation rate: {cancel_avg}%

Format each insight as a short paragraph starting with a bold header (e.g. **Revenue Leadership:**). Keep each under 2 sentences. Focus on revenue optimization, cancellation risk, and demand patterns."""


def rule_based_insights(df: pd.DataFrame) -> str:
    hotel_rev = df.groupby("hotel")["realized_booking_value"].sum()
    hotel_cancel = df.groupby("hotel")["cancellation_rate_pct"].mean()
    top_hotel = hotel_rev.idxmax()
    high_cancel_hotel = hotel_cancel.idxmax()
    peak_date = df.groupby("arrival_date")["total_bookings"].sum().idxmax()
    avg_cancel = round(df["cancellation_rate_pct"].mean(), 2)
    overall_adr = round(df["average_adr"].mean(), 2)

    return "\n\n".join([
        f"**Revenue Leadership:** {top_hotel} leads the portfolio in realized revenue — prioritize marketing spend and upsell programs here to maximize yield during peak periods.",
        f"**Cancellation Risk:** {high_cancel_hotel} carries the highest cancellation rate at {round(hotel_cancel[high_cancel_hotel], 1)}% — consider introducing non-refundable rate tiers or tightening deposit requirements to reduce revenue leakage.",
        f"**Peak Demand:** {peak_date.strftime('%B %d, %Y')} recorded the highest single-day booking volume — review upcoming dates with similar demand signals to ensure staffing and inventory are aligned.",
        f"**Yield Opportunity:** A portfolio-wide ADR of ${overall_adr} against a {avg_cancel}% cancellation rate leaves meaningful revenue on the table — A/B testing rate strategies could improve net realized revenue without sacrificing occupancy.",
    ])


def get_ai_insights(df: pd.DataFrame) -> tuple[str, bool]:
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not anthropic_key:
        return rule_based_insights(df), False
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            messages=[{"role": "user", "content": build_insights_prompt(df)}],
        )
        return message.content[0].text, True
    except Exception as e:
        return rule_based_insights(df) + f"\n\n*AI unavailable: {e}*", False


# ── Sidebar ────────────────────────────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame):
    st.sidebar.markdown("## Filters")

    hotels = sorted(df["hotel"].unique().tolist())
    selected_hotels = st.sidebar.multiselect("Hotel", hotels, default=hotels)

    min_date = df["arrival_date"].min().date()
    max_date = df["arrival_date"].max().date()
    date_range = st.sidebar.date_input(
        "Arrival Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### KPI Glossary")
    st.sidebar.caption(
        "**ADR** — Average Daily Rate: average revenue per occupied room per night.\n\n"
        "**Realized Revenue** — Revenue from completed (non-cancelled) bookings only.\n\n"
        "**Gross Booking Value** — Total value of all bookings before cancellations.\n\n"
        "**Cancellation Loss** — The gap between gross and realized revenue."
    )

    return selected_hotels, date_range


# ── Chart helpers ──────────────────────────────────────────────────────────────
COLORS = {
    "City Hotel": "#2d6a8a",
    "Resort Hotel": "#e07b39",
}
COLOR_LIST = ["#2d6a8a", "#e07b39", "#5ba87a", "#c9536a"]

# Shared light-mode layout base
def base_layout(title="", legend_bottom=True):
    layout = dict(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", size=12, color="#333"),
        title=dict(text=title, font=dict(family="Playfair Display", size=15, color="#1b3a4b"), x=0),
        margin=dict(l=12, r=12, t=48, b=52),
        xaxis=dict(showgrid=False, zeroline=False, linecolor="#e0e0e0", tickfont=dict(size=11, color="#444")),
        yaxis=dict(gridcolor="#f0ece6", zeroline=False, tickfont=dict(size=11, color="#444")),
        hoverlabel=dict(bgcolor="white", bordercolor="#ccc", font_family="Inter"),
    )
    if legend_bottom:
        layout["legend"] = dict(
            orientation="h",
            yanchor="bottom", y=-0.28,
            xanchor="left", x=0,
            font=dict(size=12, color="#333"),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        )
    return layout


def chart_bookings_over_time(df: pd.DataFrame):
    daily = (
        df.groupby(["arrival_date", "hotel"], as_index=False)["total_bookings"]
        .sum().sort_values("arrival_date")
    )
    fig = px.line(
        daily, x="arrival_date", y="total_bookings", color="hotel",
        color_discrete_map=COLORS,
        labels={"arrival_date": "", "total_bookings": "Bookings", "hotel": ""},
    )
    fig.update_traces(line_width=2)
    fig.update_layout(**base_layout("Daily Bookings by Hotel"))
    return fig


def chart_cancellation_trend(df: pd.DataFrame):
    monthly = df.copy()
    monthly["month"] = monthly["arrival_date"].dt.to_period("M").astype(str)
    trend = (
        monthly.groupby(["month", "hotel"], as_index=False)["cancellation_rate_pct"]
        .mean().sort_values("month")
    )
    fig = px.line(
        trend, x="month", y="cancellation_rate_pct", color="hotel",
        color_discrete_map=COLORS, markers=True,
        labels={"month": "", "cancellation_rate_pct": "Cancel Rate %", "hotel": ""},
    )
    fig.update_layout(**base_layout("Monthly Cancellation Rate (%)"))
    fig.update_yaxes(ticksuffix="%")
    return fig


def chart_revenue_split(df: pd.DataFrame):
    rev = df.groupby("hotel", as_index=False).agg(
        realized=("realized_booking_value", "sum"),
        gross=("gross_booking_value", "sum"),
    )
    rev["lost"] = rev["gross"] - rev["realized"]

    fig = go.Figure()
    # Realized first so it sits at the bottom (more positive story)
    fig.add_trace(go.Bar(
        name="Realized Revenue", x=rev["hotel"], y=rev["realized"],
        marker_color="#5ba87a", marker_line_width=0,
    ))
    fig.add_trace(go.Bar(
        name="Cancellation Loss", x=rev["hotel"], y=rev["lost"],
        marker_color="#e8a598", marker_line_width=0,
    ))
    layout = base_layout("Gross vs. Realized Revenue by Hotel")
    layout["barmode"] = "stack"
    layout["yaxis"]["tickprefix"] = "$"
    fig.update_layout(**layout)
    return fig


def chart_adr_box(df: pd.DataFrame):
    fig = px.box(
        df, x="hotel", y="average_adr", color="hotel",
        color_discrete_map=COLORS,
        labels={"average_adr": "ADR ($)", "hotel": ""},
    )
    fig.update_layout(**base_layout("ADR Distribution by Hotel", legend_bottom=False))
    fig.update_layout(showlegend=False)
    fig.update_yaxes(tickprefix="$")
    return fig


def chart_hotel_comparison(df: pd.DataFrame):
    metrics = df.groupby("hotel", as_index=False).agg(
        total_bookings=("total_bookings", "sum"),
        cancel_rate=("cancellation_rate_pct", "mean"),
        avg_adr=("average_adr", "mean"),
        realized_rev=("realized_booking_value", "sum"),
        nights=("total_nights_booked", "sum"),
    )

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Total Bookings", "Avg Cancellation Rate (%)"),
        horizontal_spacing=0.12,
    )
    for i, row in metrics.iterrows():
        color = COLORS.get(row["hotel"], COLOR_LIST[i % len(COLOR_LIST)])
        fig.add_trace(go.Bar(
            name=row["hotel"], x=[row["hotel"]], y=[row["total_bookings"]],
            marker_color=color, marker_line_width=0, showlegend=True,
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            name=row["hotel"], x=[row["hotel"]], y=[round(row["cancel_rate"], 2)],
            marker_color=color, marker_line_width=0, showlegend=False,
        ), row=1, col=2)

    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=12, color="#333"),
        title=dict(text="Hotel Side-by-Side Comparison", font=dict(family="Playfair Display", size=15, color="#1b3a4b"), x=0),
        margin=dict(l=12, r=12, t=56, b=52),
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="left", x=0, font=dict(size=12, color="#333"), bgcolor="rgba(0,0,0,0)", borderwidth=0),
        hoverlabel=dict(bgcolor="white", bordercolor="#ccc", font_family="Inter"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#e0e0e0")
    fig.update_yaxes(gridcolor="#f0ece6", zeroline=False)
    fig.update_yaxes(ticksuffix="%", row=1, col=2)

    return fig, metrics


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    df_full = load_data()
    selected_hotels, date_range = render_sidebar(df_full)

    # Apply filters
    df = df_full[df_full["hotel"].isin(selected_hotels)].copy()
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        df = df[(df["arrival_date"] >= start) & (df["arrival_date"] <= end)]

    # ── Hero header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <p class="hero-title">Hospitality Analytics</p>
        <p class="hero-subtitle">Hotel booking performance powered by Databricks Lakehouse</p>
        <span class="hero-badge">Databricks</span>
        <span class="hero-badge">Gold Layer</span>
        <span class="hero-badge">2015 – 2017</span>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("No data matches the current filters.")
        return

    # ── KPIs ───────────────────────────────────────────────────────────────────
    total_bookings = int(df["total_bookings"].sum())
    cancel_rate = round(df["cancellation_rate_pct"].mean(), 2)
    avg_adr = round(df["average_adr"].mean(), 2)
    realized_rev = int(df["realized_booking_value"].sum())
    gross_rev = int(df["gross_booking_value"].sum())
    cancellation_loss = gross_rev - realized_rev
    loss_pct = round(cancellation_loss / gross_rev * 100, 1) if gross_rev else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Bookings", f"{total_bookings:,}")
    k2.metric("Cancellation Rate", f"{cancel_rate}%")
    k3.metric("Average ADR", f"${avg_adr:,.2f}")
    k4.metric("Realized Revenue", f"${realized_rev:,}")
    k5.metric("Cancellation Loss", f"${cancellation_loss:,}", delta=f"-{loss_pct}% of gross", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI Insights ────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">AI Insight Summary</p>', unsafe_allow_html=True)
    st.markdown("---")

    with st.spinner("Analyzing data..."):
        insights_text, is_ai = get_ai_insights(df)

    # Render markdown to HTML manually so it works inside a styled div
    import re
    def md_to_html(text: str) -> str:
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        paragraphs = text.strip().split("\n\n")
        return "".join(f"<p style='margin:0 0 0.9rem 0'>{p.strip()}</p>" for p in paragraphs)

    st.markdown(
        f'<div class="insight-box">{md_to_html(insights_text)}</div>',
        unsafe_allow_html=True,
    )

    badge = "Claude AI" if is_ai else "Rule-based analysis"
    st.caption(f"Source: {badge} · {len(df):,} rows · {df['arrival_date'].min().date()} to {df['arrival_date'].max().date()}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Trends ─────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Trends</p>', unsafe_allow_html=True)
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(chart_bookings_over_time(df), use_container_width=True)
    with c2:
        st.plotly_chart(chart_cancellation_trend(df), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(chart_revenue_split(df), use_container_width=True)
    with c4:
        st.plotly_chart(chart_adr_box(df), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Exploration ────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Exploration</p>', unsafe_allow_html=True)
    st.markdown("---")

    comp_fig, comp_metrics = chart_hotel_comparison(df)
    st.plotly_chart(comp_fig, use_container_width=True)

    st.markdown("##### Hotel Summary")
    display = comp_metrics.copy()
    display.columns = ["Hotel", "Total Bookings", "Avg Cancel Rate (%)", "Avg ADR ($)", "Realized Revenue ($)", "Total Nights"]
    display["Avg Cancel Rate (%)"] = display["Avg Cancel Rate (%)"].round(2)
    display["Avg ADR ($)"] = display["Avg ADR ($)"].round(2)
    display["Realized Revenue ($)"] = display["Realized Revenue ($)"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    with st.expander("Raw data explorer"):
        sort_col = st.selectbox("Sort by", df.columns.tolist(), index=0)
        asc = st.radio("Order", ["Ascending", "Descending"], horizontal=True) == "Ascending"
        st.dataframe(df.sort_values(sort_col, ascending=asc).reset_index(drop=True), use_container_width=True)


if __name__ == "__main__":
    main()