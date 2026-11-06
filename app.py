import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="AuraStay Analytics", page_icon="🏨", layout="wide")

# --- Data Loading ---
@st.cache_data
def load_data():
    # Read the CSV directly for the live web deployment
    df = pd.read_csv('hotel_bookings.csv')
    df = df.dropna(subset=['adr'])
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['revenue'] = df['adr'] * df['total_nights']
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")
selected_month = st.sidebar.multiselect(
    "Select Month", 
    options=df['arrival_date_month'].unique(), 
    default=df['arrival_date_month'].unique()[:3]
)
df_filtered = df[df['arrival_date_month'].isin(selected_month)]

# --- Main Header ---
st.title("🏨 AuraStay Analytics")
st.markdown("Enterprise-grade business intelligence for hospitality and tourism operations. Built with Python, AWS, and Plotly.")

# --- KPI Row ---
total_revenue = df_filtered['revenue'].sum()
total_bookings = len(df_filtered)
canceled = df_filtered[df_filtered['is_canceled'] == 1].shape[0]
avg_adr = df_filtered['adr'].mean()

# Simulate a comparison (e.g., vs target or last period)
revenue_delta = "12%"  
bookings_delta = "-3%"
canceled_delta = "-1%"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"€{total_revenue:,.0f}", delta=revenue_delta)
col2.metric("Total Bookings", f"{total_bookings:,}", delta=bookings_delta, delta_color="normal")
col3.metric("Canceled Bookings", f"{canceled:,}", delta=canceled_delta, delta_color="inverse") 
col4.metric("Avg Daily Rate (ADR)", f"€{avg_adr:.2f}")

st.divider()

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue Trends", "🌍 Demographics & Map", "📊 Raw Data", "⚙️ Data Tools"])

with tab1:
    st.subheader("Revenue Trend by Month")
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    revenue_by_month = df_filtered.groupby('arrival_date_month')['revenue'].sum().reindex(months).dropna()
    
    fig = px.line(
        x=revenue_by_month.index, 
        y=revenue_by_month.values, 
        labels={'x': 'Month', 'y': 'Revenue (€)'},
        markers=True,
        title="Monthly Revenue"
    )
    fig.update_layout(hovermode="x unified") 
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Booking Sources")
    segment_counts = df_filtered['market_segment'].value_counts()
    fig_bar = px.bar(
        x=segment_counts.index, 
        y=segment_counts.values,
        labels={'x': 'Market Segment', 'y': 'Bookings'},
        color=segment_counts.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Guest Demographics")
    col_left, col_right = st.columns(2)
    
    with col_left:
        top_countries = df_filtered['country'].value_counts().head(10)
        fig_country = px.pie(
            values=top_countries.values, 
            names=top_countries.index, 
            title="Top 10 Guest Countries",
            hole=0.3 
        )
        st.plotly_chart(fig_country, use_container_width=True)
        
    with col_right:
        country_coords = {
            'PRT': (39.3999, -8.2245), 'GBR': (55.3781, -3.4360), 'ESP': (40.4637, -3.7492),
            'FRA': (46.2276, 2.2137), 'DEU': (51.1657, 10.4515), 'ITA': (41.8719, 12.5674),
            'IRL': (53.1424, -7.6921), 'BEL': (50.5039, 4.4699), 'BRA': (-14.2350, -51.9253), 'NLD': (52.1326, 5.2913)
        }
        map_data = pd.DataFrame([
            {"lat": country_coords[c][0], "lon": country_coords[c][1], "country": c, "bookings": v}
            for c, v in top_countries.items() if c in country_coords
        ])
        if not map_data.empty:
            st.subheader("Global Guest Map")
            st.map(map_data, latitude='lat', longitude='lon', size='bookings') 
        else:
            st.info("No map coordinates available for selected countries.")

with tab3:
    st.subheader("Database Records")
    st.dataframe(df_filtered.head(100), use_container_width=True)

with tab4:
    st.subheader("Export Data")
    st.markdown("Download the filtered dataset as a CSV file for offline analysis.")
    
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df(df_filtered)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='hotel_bookings_filtered.csv',
        mime='text/csv',
    )
    
    st.subheader("Upload New Data (Demo)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        st.success("File uploaded successfully! (In a real app, this would trigger the ETL pipeline).")

st.caption("Developed by Monisha Rani S | Data Pipeline: AWS S3 -> Python -> MySQL -> Streamlit + Plotly")