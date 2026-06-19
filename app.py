import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Ride Performance Monitoring System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Look
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 15px;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
        border-color: #475569;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 8px 0;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        line-height: 1;
    }
    .metric-subtitle {
        color: #64748b;
        font-size: 11px;
        margin: 6px 0 0 0;
    }
    
    /* Recommendations Box styling */
    .recommendation-box {
        background-color: #1e293b;
        border-left: 4px solid #10b981;
        padding: 15px;
        border-radius: 4px 8px 8px 4px;
        margin-bottom: 10px;
        border: 1px solid #334155;
        border-left-width: 4px;
    }
    .recommendation-title {
        color: #e2e8f0;
        font-weight: 700;
        margin: 0 0 5px 0;
        font-size: 15px;
    }
    .recommendation-desc {
        color: #94a3b8;
        font-size: 13px;
        margin: 0;
    }
    
    /* Highlight styles */
    .val-green { color: #10b981; }
    .val-blue { color: #3b82f6; }
    .val-indigo { color: #6366f1; }
    .val-amber { color: #f59e0b; }
    .val-rose { color: #f43f5e; }
    
    /* Main title styling */
    .main-title {
        background: linear-gradient(90deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ride_performance.db")

# Database Connection Helper
def get_connection():
    return sqlite3.connect(DB_PATH)

# Load Data
@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found at {DB_PATH}. Please run database initialization first.")
        return pd.DataFrame()
    
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM rides1", conn)
    conn.close()
    
    # Preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    # Convert numeric columns explicitly
    df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce')
    df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce')
    df['Driver_Ratings'] = pd.to_numeric(df['Driver_Ratings'], errors='coerce')
    df['Customer_Rating'] = pd.to_numeric(df['Customer_Rating'], errors='coerce')
    return df

df_raw = load_data()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.markdown("<h2 style='color: #3b82f6; margin-bottom: 0;'>🚗 RideSync</h2>", unsafe_allow_html=True)
st.sidebar.title("Dashboard Controls")
st.sidebar.write("Filter metrics across dimensions:")

if not df_raw.empty:
    # Reset Filters button
    if st.sidebar.button("🔄 Reset All Filters"):
        st.cache_data.clear()
        st.rerun()

    # Date Range Filter
    min_date = df_raw['Date'].min().date()
    max_date = df_raw['Date'].max().date()
    
    st.sidebar.subheader("📅 Date Range")
    start_date, end_date = st.sidebar.date_input(
        "Select Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Vehicle Type Filter
    st.sidebar.subheader("🚗 Vehicle Type")
    vehicle_types = sorted(df_raw['Vehicle_Type'].dropna().unique())
    selected_vehicles = st.sidebar.multiselect(
        "Select Vehicles",
        options=vehicle_types,
        default=vehicle_types
    )
    
    # Booking Status Filter
    st.sidebar.subheader("📊 Booking Status")
    booking_statuses = sorted(df_raw['Booking_Status'].dropna().unique())
    selected_statuses = st.sidebar.multiselect(
        "Select Statuses",
        options=booking_statuses,
        default=booking_statuses
    )
    
    # Payment Method Filter
    st.sidebar.subheader("💳 Payment Method")
    payment_methods = sorted(df_raw['Payment_Method'].dropna().unique())
    selected_payments = st.sidebar.multiselect(
        "Select Payments",
        options=payment_methods,
        default=payment_methods
    )
    
    # Apply Filters
    mask = (
        (df_raw['Date'].dt.date >= start_date) & 
        (df_raw['Date'].dt.date <= end_date) &
        (df_raw['Vehicle_Type'].isin(selected_vehicles)) &
        (df_raw['Booking_Status'].isin(selected_statuses))
    )
    if len(selected_payments) < len(payment_methods):
        mask = mask & (df_raw['Payment_Method'].isin(selected_payments))
        
    df_filtered = df_raw[mask]
else:
    df_filtered = pd.DataFrame()

# ----------------- MAIN INTERFACE -----------------
st.markdown('<div class="main-title">🚗 Ride Performance Monitoring System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive business intelligence, SQL analytical workspace & optimization engine</div>', unsafe_allow_html=True)

# Tabs
tab_kpi, tab_insights, tab_sql, tab_data, tab_showcase = st.tabs([
    "📈 Interactive KPIs & Visuals", 
    "💡 Smart Insights & Simulator",
    "💻 SQL Analytics Studio", 
    "📂 Dataset Explorer",
    "🖼️ Original Dashboards"
])

# ----------------- TAB 1: INTERACTIVE KPIS & VISUALS -----------------
with tab_kpi:
    if df_filtered.empty:
        st.warning("No data available with the current filter settings. Please adjust your filters in the sidebar.")
    else:
        # Metrics Calculations
        total_bookings = len(df_filtered)
        success_bookings = df_filtered[df_filtered['Booking_Status'] == 'Success']
        total_success = len(success_bookings)
        success_rate = (total_success / total_bookings * 100) if total_bookings > 0 else 0
        
        total_revenue = success_bookings['Booking_Value'].sum()
        avg_distance = df_filtered['Ride_Distance'].mean()
        avg_cust_rating = df_filtered['Customer_Rating'].dropna().mean()
        avg_dr_rating = df_filtered['Driver_Ratings'].dropna().mean()
        
        # Grid of KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Bookings</div>
                <div class="metric-value val-blue">{total_bookings:,}</div>
                <div class="metric-subtitle">Across selected filters</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Revenue</div>
                <div class="metric-value val-green">₹{total_revenue / 1e6:.2f}M</div>
                <div class="metric-subtitle">Successful bookings sum</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Success Rate</div>
                <div class="metric-value val-indigo">{success_rate:.2f}%</div>
                <div class="metric-subtitle">{total_success:,} completed rides</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Avg Distance</div>
                <div class="metric-value val-amber">{avg_distance:.2f} km</div>
                <div class="metric-subtitle">Per ride average</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Avg Ratings</div>
                <div class="metric-value val-rose">⭐ {avg_cust_rating:.2f} / {avg_dr_rating:.2f}</div>
                <div class="metric-subtitle">Customer / Driver averages</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Row 1: Charts
        col_c1, col_c2 = st.columns([1, 1])

        with col_c1:
            st.subheader("📊 Booking Status Breakdown")
            status_counts = df_filtered['Booking_Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            color_map = {
                'Success': '#10B981',
                'Canceled by Customer': '#EF4444',
                'Canceled by Driver': '#F59E0B',
                'Driver Not Found': '#6B7280'
            }
            
            fig_status = px.pie(
                status_counts, 
                values='Count', 
                names='Status', 
                hole=0.45,
                color='Status',
                color_discrete_map=color_map,
                category_orders={"Status": ['Success', 'Canceled by Customer', 'Canceled by Driver', 'Driver Not Found']}
            )
            fig_status.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                margin=dict(t=20, b=50, l=10, r=10),
                height=350
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with col_c2:
            st.subheader("🚗 Vehicle Type Performance")
            v_perf = df_filtered.groupby('Vehicle_Type').agg(
                Revenue=('Booking_Value', lambda x: x[df_filtered.loc[x.index, 'Booking_Status'] == 'Success'].sum()),
                Bookings=('Booking_ID', 'count')
            ).reset_index()
            v_perf = v_perf.sort_values(by='Revenue', ascending=True)
            
            fig_v_perf = go.Figure()
            fig_v_perf.add_trace(go.Bar(
                y=v_perf['Vehicle_Type'],
                x=v_perf['Bookings'],
                name='Bookings Count',
                orientation='h',
                marker=dict(color='#3b82f6'),
                xaxis='x'
            ))
            fig_v_perf.add_trace(go.Bar(
                y=v_perf['Vehicle_Type'],
                x=v_perf['Revenue'],
                name='Revenue (₹)',
                orientation='h',
                marker=dict(color='#10b981'),
                xaxis='x2'
            ))
            
            fig_v_perf.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=40, l=10, r=10),
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                xaxis=dict(title='Bookings Count', title_font=dict(color='#3b82f6'), tickfont=dict(color='#3b82f6')),
                xaxis2=dict(title='Revenue (₹)', title_font=dict(color='#10b981'), tickfont=dict(color='#10b981'), overlaying='x', side='top')
            )
            st.plotly_chart(fig_v_perf, use_container_width=True)

        # Row 2: Charts
        col_c3, col_c4 = st.columns([1, 1])

        with col_c3:
            st.subheader("❌ Customer vs. Driver Cancellation Reasons")
            cust_cancel = df_filtered['Canceled_Rides_by_Customer'].value_counts().reset_index()
            cust_cancel.columns = ['Reason', 'Count']
            cust_cancel['Type'] = 'Customer Cancel'
            
            driver_cancel = df_filtered['Canceled_Rides_by_Driver'].value_counts().reset_index()
            driver_cancel.columns = ['Reason', 'Count']
            driver_cancel['Type'] = 'Driver Cancel'
            
            cancel_df = pd.concat([cust_cancel, driver_cancel], ignore_index=True)
            
            fig_cancel = px.bar(
                cancel_df,
                x='Count',
                y='Reason',
                color='Type',
                orientation='h',
                barmode='group',
                color_discrete_map={'Customer Cancel': '#f43f5e', 'Driver Cancel': '#f59e0b'}
            )
            fig_cancel.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=40, l=10, r=10),
                height=350,
                yaxis=dict(autorange="reversed"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_cancel, use_container_width=True)

        with col_c4:
            st.subheader("📈 Hourly Booking Velocity")
            df_filtered['Hour'] = df_filtered['Date'].dt.hour
            hourly_trends = df_filtered.groupby(['Hour', 'Booking_Status']).size().reset_index(name='Rides')
            
            fig_hourly = px.line(
                hourly_trends,
                x='Hour',
                y='Rides',
                color='Booking_Status',
                markers=True,
                color_discrete_map=color_map
            )
            fig_hourly.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(dtick=2, title="Hour of Day (24h)"),
                yaxis=dict(title="Number of Rides"),
                margin=dict(t=20, b=40, l=10, r=10),
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_hourly, use_container_width=True)

# ----------------- TAB 2: SMART INSIGHTS & SIMULATOR -----------------
with tab_insights:
    st.subheader("💡 Advanced Analytics & What-If Business Simulator")
    st.write("Understand the financial impact of operational optimizations and discover booking hotspots.")
    
    if df_filtered.empty:
        st.warning("Please adjust your filters to load the dataset for simulation.")
    else:
        # What-If Revenue Simulator Column Setup
        col_sim1, col_sim2 = st.columns([1, 2])
        
        with col_sim1:
            st.markdown("### 🎛️ Simulator Parameters")
            st.write("Adjust sliders to estimate potential revenue gains from solving operational pain points:")
            
            # Base numbers
            total_cancel = df_filtered[df_filtered['Booking_Status'].str.contains('Canceled', case=False, na=False)].shape[0]
            success_count = df_filtered[df_filtered['Booking_Status'] == 'Success'].shape[0]
            success_rev = df_filtered[df_filtered['Booking_Status'] == 'Success']['Booking_Value'].sum()
            avg_val_success = df_filtered[df_filtered['Booking_Status'] == 'Success']['Booking_Value'].mean()
            if pd.isna(avg_val_success): avg_val_success = 0
            
            recovery_rate = st.slider(
                "Recover Canceled Bookings (%)", 
                min_value=0, max_value=100, value=20, step=5,
                help="Percentage of customer & driver cancellations converted into successful completed rides."
            )
            
            price_adjustment = st.slider(
                "Optimize Average Booking Value (%)", 
                min_value=-10, max_value=30, value=5, step=1,
                help="Potential increase in fare/booking value through route optimization or dynamic surge pricing."
            )
            
            # Calculations
            recovered_rides = int(total_cancel * (recovery_rate / 100))
            sim_success_count = success_count + recovered_rides
            recovered_revenue = recovered_rides * avg_val_success
            
            simulated_revenue = (success_rev + recovered_revenue) * (1 + (price_adjustment / 100))
            revenue_lift = simulated_revenue - success_rev
            
            st.markdown("---")
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #064e3b, #022c22); border-color: #059669;">
                <div class="metric-title" style="color: #a7f3d0;">Simulated Revenue Lift</div>
                <div class="metric-value val-green">₹{revenue_lift / 1e6:.2f}M</div>
                <div class="metric-subtitle" style="color: #6ee7b7;">+{revenue_lift/success_rev*100:.1f}% Revenue Growth</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Recovered Rides:** `{recovered_rides:,}` canceled rides converted.")
            
        with col_sim2:
            st.markdown("### 📊 Revenue Comparison")
            
            fig_sim = go.Figure()
            fig_sim.add_trace(go.Bar(
                x=['Current Revenue', 'Simulated Revenue'],
                y=[success_rev, simulated_revenue],
                text=[f"₹{success_rev/1e6:.2f}M", f"₹{simulated_revenue/1e6:.2f}M"],
                textposition='auto',
                marker_color=['#475569', '#10b981']
            ))
            fig_sim.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title="Revenue (₹)", showgrid=True, gridcolor='#334155'),
                xaxis=dict(tickfont=dict(size=14, color='#f8fafc')),
                height=300,
                margin=dict(t=20, b=20, l=10, r=10)
            )
            st.plotly_chart(fig_sim, use_container_width=True)
            
            # Recommendation output based on calculations
            st.markdown("### 💡 Recommended Actions")
            if recovery_rate > 0:
                st.markdown(f"""
                <div class="recommendation-box">
                    <div class="recommendation-title">🎯 Recovery Action Plan (Target: {recovery_rate}%)</div>
                    <div class="recommendation-desc">
                        To capture the additional <b>₹{recovered_revenue/1e6:.2f}M</b> from recovered cancellations, implement driver-side retention incentives for <i>'Personal & Car issues'</i> (top driver cancel reason) and optimize customer wait times to prevent <i>'Driver is taking too long'</i> cancellations.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            if price_adjustment > 0:
                st.markdown(f"""
                <div class="recommendation-box" style="border-left-color: #3b82f6;">
                    <div class="recommendation-title">⚡ Surge & Route Pricing (Target: +{price_adjustment}%)</div>
                    <div class="recommendation-desc">
                        Increase ride prices by <b>{price_adjustment}%</b> selectively during high-demand/high-cancellation intervals (e.g. late night peaks) via dynamic surge multipliers. This also serves to incentivize driver supply when it's needed most.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Row 2: Hotspot analysis
        st.subheader("📍 Demand Hotspots & Key Routes")
        col_hot1, col_hot2 = st.columns(2)
        
        with col_hot1:
            st.markdown("**Top Pickup Locations (by Successful Bookings & Revenue)**")
            pickup_data = df_filtered[df_filtered['Booking_Status'] == 'Success'].groupby('Pickup_Location').agg(
                Bookings=('Booking_ID', 'count'),
                Revenue=('Booking_Value', 'sum')
            ).reset_index().sort_values(by='Bookings', ascending=False).head(5)
            
            fig_hot_p = px.bar(
                pickup_data, x='Pickup_Location', y='Bookings',
                color='Revenue', color_continuous_scale='Viridis',
                labels={'Bookings': 'Successful Bookings', 'Pickup_Location': 'Pickup Area'}
            )
            fig_hot_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig_hot_p, use_container_width=True)
            
        with col_hot2:
            st.markdown("**Top Routes (Pickup ➔ Drop-off)**")
            route_data = df_filtered[df_filtered['Booking_Status'] == 'Success'].groupby(['Pickup_Location', 'Drop_Location']).agg(
                Bookings=('Booking_ID', 'count'),
                Revenue=('Booking_Value', 'sum')
            ).reset_index()
            route_data['Route'] = route_data['Pickup_Location'] + " ➔ " + route_data['Drop_Location']
            route_data = route_data.sort_values(by='Bookings', ascending=False).head(5)
            
            fig_hot_r = px.bar(
                route_data, y='Route', x='Bookings',
                color='Revenue', color_continuous_scale='Cividis',
                orientation='h',
                labels={'Bookings': 'Successful Bookings', 'Route': 'Route (From ➔ To)'}
            )
            fig_hot_r.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_hot_r, use_container_width=True)

# ----------------- TAB 3: SQL ANALYTICS STUDIO -----------------
with tab_sql:
    st.subheader("💻 Executing SQL queries on local Database")
    st.write("Browse and run pre-defined SQL queries, use the visual SQL query wizard builder, or enter custom query scripts.")
    
    # Pre-defined Queries
    predefined_queries = {
        "1. Retrieve all successful bookings": {
            "sql": "SELECT * FROM succesfull_booking LIMIT 100;",
            "desc": "Retrieves the first 100 successful bookings from the view created by Query #1."
        },
        "2. Find the average ride distance for each vehicle type": {
            "sql": "SELECT * FROM avg_ride_distance_for_each_vehicle_types;",
            "desc": "Calculates and returns the average ride distance grouped by each type of vehicle."
        },
        "3. Get the total number of cancelled rides by customers": {
            "sql": "SELECT * FROM rides_cancelled_by_customer;",
            "desc": "Calculates the sum of bookings cancelled directly by the customer."
        },
        "4. List the top 5 customers who booked the highest number of rides": {
            "sql": "SELECT * FROM top_5_customers;",
            "desc": "Identifies the top 5 Customer IDs with the highest number of bookings."
        },
        "5. Get driver cancellations due to personal/car issues": {
            "sql": "SELECT * FROM Rides_cancelled_by_Drivers_P_C_Issues;",
            "desc": "Calculates the count of driver-initiated cancellations specifically due to 'Personal & Car related issue'."
        },
        "6. Find min & max driver ratings for Prime Sedan": {
            "sql": "SELECT * FROM Max_Min_Driver_Rating;",
            "desc": "Finds the lowest and highest driver rating for 'Prime Sedan' bookings."
        },
        "7. Retrieve all UPI payments": {
            "sql": "SELECT * FROM upi_payments LIMIT 100;",
            "desc": "Retrieves the first 100 ride bookings where the payment method was 'UPI'."
        },
        "8. Find average customer rating per vehicle type": {
            "sql": "SELECT * FROM AVG_Cust_Rating;",
            "desc": "Calculates the average rating given by customers for each vehicle type."
        },
        "9. Calculate total booking value of successful rides": {
            "sql": "SELECT * FROM total_successful_ride_value;",
            "desc": "Calculates the total booking value (revenue) generated by completed bookings."
        },
        "10. List incomplete rides along with reason": {
            "sql": "SELECT * FROM Incomplete_Rides_Reason LIMIT 100;",
            "desc": "Retrieves the first 100 rides that were marked as incomplete, detailing the specific reason."
        }
    }

    col_sql1, col_sql2 = st.columns([1, 2])
    
    with col_sql1:
        st.markdown("### 🛠️ Visual SQL Query Wizard")
        st.write("Generate SQL commands automatically without coding:")
        
        wiz_metric = st.selectbox(
            "Select Metric (Aggregate)",
            options=["Total Bookings", "Total Revenue", "Average Ride Distance", "Average Customer Rating", "Average Driver Rating"]
        )
        
        wiz_group = st.selectbox(
            "Group By Dimension",
            options=["Vehicle Type", "Payment Method", "Booking Status", "Pickup Location", "Drop Location"]
        )
        
        # Build SQL Query String
        metrics_sql_map = {
            "Total Bookings": "COUNT(Booking_ID) AS Total_Bookings",
            "Total Revenue": "SUM(Booking_Value) AS Total_Revenue",
            "Average Ride Distance": "ROUND(AVG(Ride_Distance), 2) AS Avg_Distance_KM",
            "Average Customer Rating": "ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating",
            "Average Driver Rating": "ROUND(AVG(Driver_Ratings), 2) AS Avg_Driver_Rating"
        }
        
        group_sql_map = {
            "Vehicle Type": "Vehicle_Type",
            "Payment Method": "Payment_Method",
            "Booking Status": "Booking_Status",
            "Pickup Location": "Pickup_Location",
            "Drop Location": "Drop_Location"
        }
        
        sel_metric_sql = metrics_sql_map[wiz_metric]
        sel_group_sql = group_sql_map[wiz_group]
        
        # Add success filter for revenue to be mathematically accurate
        where_clause = ""
        if wiz_metric == "Total Revenue":
            where_clause = " WHERE Booking_Status = 'Success'"
            
        generated_sql = f"SELECT {sel_group_sql}, {sel_metric_sql} \nFROM rides1{where_clause} \nGROUP BY {sel_group_sql} \nORDER BY 2 DESC;"
        
        st.info("💡 To run the wizard-generated SQL, click the button below to load it into the editor.")
        if st.button("📥 Load Wizard SQL into Editor"):
            sql_editor_val = generated_sql
        else:
            sql_editor_val = None

        st.markdown("---")
        
        # Predefined Select
        st.markdown("### 📋 Predefined SQL Select")
        query_selection = st.selectbox(
            "Select an query template:",
            options=["-- Select a Template --"] + list(predefined_queries.keys())
        )
        
        if query_selection != "-- Select a Template --":
            selected_query_details = predefined_queries[query_selection]
            sql_editor_val = selected_query_details["sql"]
            st.caption(f"**Template Description:** {selected_query_details['desc']}")

    with col_sql2:
        st.markdown("### 📝 SQL Query Editor")
        
        if sql_editor_val is None:
            sql_editor_val = "SELECT * FROM rides1 LIMIT 10;"
            
        custom_sql = st.text_area(
            "Enter SQLite compatible SQL query script:",
            value=sql_editor_val,
            height=160
        )
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            run_btn = st.button("🚀 Execute Query", key="exec_sql_btn", use_container_width=True)
        with col_act2:
            # Quick copy/clean helper
            clear_btn = st.button("🧹 Clear Editor", use_container_width=True)
            if clear_btn:
                custom_sql = "SELECT * FROM rides1 LIMIT 10;"
                st.rerun()

        # Database Schema help
        with st.expander("📚 Database Schema Reference (Click to expand)"):
            st.write("Use these column names in your SQL queries. All text columns are case-insensitive.")
            schema_data = [
                {"Column Name": "Booking_ID", "Type": "TEXT", "Description": "Unique identifier of the ride booking."},
                {"Column Name": "Date", "Type": "TEXT/DATETIME", "Description": "Date of the ride creation (YYYY-MM-DD HH:MM:DD)."},
                {"Column Name": "Booking_Status", "Type": "TEXT (NOCASE)", "Description": "Booking status ('Success', 'Canceled by Customer', etc.)"},
                {"Column Name": "Customer_ID", "Type": "TEXT", "Description": "Unique identifier of the customer."},
                {"Column Name": "Vehicle_Type", "Type": "TEXT (NOCASE)", "Description": "Vehicle type ('Prime Sedan', 'Bike', 'Auto', etc.)"},
                {"Column Name": "Pickup_Location / Drop_Location", "Type": "TEXT", "Description": "Pickup and drop locations."},
                {"Column Name": "Booking_Value", "Type": "REAL", "Description": "Fare amount of the ride booking in INR (₹)."},
                {"Column Name": "Payment_Method", "Type": "TEXT (NOCASE)", "Description": "Payment method ('UPI', 'Cash', 'Credit Card', 'Debit Card')"},
                {"Column Name": "Ride_Distance", "Type": "REAL", "Description": "Distance traveled in kilometers (km)."},
                {"Column Name": "Driver_Ratings / Customer_Rating", "Type": "REAL", "Description": "Ratings given out of 5 stars."}
            ]
            st.table(schema_data)
            
        if run_btn:
            if custom_sql.strip():
                with st.spinner("Executing SQL query against local SQLite..."):
                    try:
                        conn = get_connection()
                        res_df = pd.read_sql(custom_sql, conn)
                        conn.close()
                        
                        st.success(f"Query executed successfully! Returned {len(res_df)} rows.")
                        st.dataframe(res_df, use_container_width=True)
                        
                        # Download SQL Results
                        res_csv = res_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Query Results as CSV",
                            data=res_csv,
                            file_name="sql_query_results.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"SQL Error: {e}")
            else:
                st.error("Please enter a non-empty SQL query to execute.")

# ----------------- TAB 4: DATASET EXPLORER -----------------
with tab_data:
    st.subheader("📂 Raw Dataset Explorer")
    st.write("Browse, filter, and inspect the raw dataset containing ride-level details.")
    
    if not df_raw.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search_col = st.selectbox("Search Column", options=["Booking_ID", "Customer_ID", "Pickup_Location", "Drop_Location"])
        with col_f2:
            search_term = st.text_input(f"Enter search query for {search_col}:")
            
        explore_df = df_raw.copy()
        if search_term:
            explore_df = explore_df[explore_df[search_col].astype(str).str.contains(search_term, case=False, na=False)]
            
        st.write(f"Showing {min(len(explore_df), 500)} of {len(explore_df)} records:")
        st.dataframe(explore_df.head(500), use_container_width=True)
        
        # Download button
        csv_data = explore_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv_data,
            file_name="ride_performance_dataset_filtered.csv",
            mime="text/csv"
        )
        
        # Statistics summary
        with st.expander("📊 View Data Columns & Statistics Summary"):
            st.write(explore_df.describe(include='all'))
    else:
        st.error("Dataset not loaded. Make sure the database exists.")

# ----------------- TAB 5: ORIGINAL DASHBOARDS -----------------
with tab_showcase:
    st.subheader("🖼️ Original Power BI Dashboard Showcase")
    st.write("Below are the high-fidelity exports and screenshots from the original Power BI dashboard project.")
    
    images_info = [
        {"title": "🖥️ Main Dashboard Overview", "file": "Screenshot 2025-03-26 164037.png", "desc": "High-level summary of Bookings, Revenue, and Key KPIs."},
        {"title": "🏎️ Vehicle Type Analysis", "file": "dashboard  _vechicle type_analysis .png", "desc": "Analysis of booking volume, average distance, and ratings across vehicle segments."},
        {"title": "💰 Revenue Analysis", "file": "dashboard_Revenue_analysis.png", "desc": "Detailed breakdown of monthly/daily revenue, payments, and booking values."},
        {"title": "❌ Cancellation Insights", "file": "dashboard_Cancellation_analysis.png", "desc": "Visualization of customer-initiated vs. driver-initiated cancellation patterns and reasons."},
        {"title": "⭐ Customer Satisfaction (Ratings)", "file": "Dashboard_Rating_analysis.png", "desc": "Analysis of customer ratings and driver ratings distribution."}
    ]
    
    for img_info in images_info:
        st.markdown(f"### {img_info['title']}")
        st.write(img_info['desc'])
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_info['file'])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
        else:
            st.warning(f"Screenshot file '{img_info['file']}' could not be located in the workspace.")
        st.markdown("---")
