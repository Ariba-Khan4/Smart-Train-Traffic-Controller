import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Configuration
BACKEND_URL = "http://backend:8000"

# Page configuration
st.set_page_config(
    page_title="Smart Train Traffic Controller",
    page_icon="🚂",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .delayed-train {
        background-color: #ffebee;
        padding: 1rem;
        border-left: 5px solid #f44336;
        margin: 0.5rem 0;
    }
    .on-time-train {
        background-color: #e8f5e9;
        padding: 1rem;
        border-left: 5px solid #4caf50;
        margin: 0.5rem 0;
    }
    .rerouted-train {
        background-color: #fff3e0;
        padding: 1rem;
        border-left: 5px solid #ff9800;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚂 Smart Train Traffic Controller</h1>', unsafe_allow_html=True)
st.markdown("**Railway Automation System** | Delay Prediction & Intelligent Rerouting")

# Sidebar
st.sidebar.title("⚙️ Control Panel")
mode = st.sidebar.radio("Select Mode", ["Dashboard", "Delay Predictor", "Rerouting Engine", "Upload Schedule"])

# Check backend health
try:
    health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if health_response.status_code == 200:
        st.sidebar.success("✅ Backend: Online")
    else:
        st.sidebar.error("❌ Backend: Error")
except:
    st.sidebar.error("❌ Backend: Offline")

# Mode 1: Dashboard
if mode == "Dashboard":
    st.header("📊 Live Train Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trains", "50", "+5")
    with col2:
        st.metric("On Time", "40", "-2")
    with col3:
        st.metric("Delayed", "10", "+7")
    with col4:
        st.metric("Avg Delay", "25 min", "+5 min")
    
    # Fetch trains
    try:
        response = requests.get(f"{BACKEND_URL}/trains")
        if response.status_code == 200:
            trains_data = response.json()["trains"]
            df = pd.DataFrame(trains_data)
            
            # Filter controls
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect("Filter by Status", df["status"].unique(), default=df["status"].unique())
            with col2:
                source_filter = st.multiselect("Filter by Source", df["source"].unique(), default=df["source"].unique())
            
            # Apply filters
            filtered_df = df[(df["status"].isin(status_filter)) & (df["source"].isin(source_filter))]
            
            # Display trains
            st.subheader(f"🚆 Active Trains ({len(filtered_df)})")
            
            for idx, row in filtered_df.iterrows():
                if row["status"] == "Delayed":
                    css_class = "delayed-train"
                    icon = "🔴"
                else:
                    css_class = "on-time-train"
                    icon = "🟢"
                
                st.markdown(f"""
                <div class="{css_class}">
                    {icon} <strong>{row['train_id']}</strong> - {row['train_name']}<br>
                    📍 {row['source']} → {row['destination']}<br>
                    ⏰ Departure: {row['scheduled_departure']} | Platform: {row['platform']}
                </div>
                """, unsafe_allow_html=True)
            
            # Show dataframe
            with st.expander("📋 View Full Schedule"):
                st.dataframe(filtered_df, use_container_width=True)
        else:
            st.error("Failed to fetch train data")
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")

# Mode 2: Delay Predictor
elif mode == "Delay Predictor":
    st.header("🔮 Delay Prediction Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        train_id = st.text_input("Train ID", "TR0001")
        station = st.text_input("Current Station", "Mumbai")
        weather = st.selectbox("Weather Condition", ["clear", "cloudy", "rain", "storm", "fog"])
    
    with col2:
        current_time = st.time_input("Current Time", datetime.now().time())
        day_of_week = st.selectbox("Day of Week", list(range(7)), format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x])
    
    if st.button("🔍 Predict Delay", type="primary"):
        with st.spinner("Analyzing train conditions..."):
            time.sleep(1)
            
            try:
                payload = {
                    "train_id": train_id,
                    "current_time": current_time.strftime("%H:%M"),
                    "station": station,
                    "weather_condition": weather,
                    "day_of_week": day_of_week
                }
                
                response = requests.post(f"{BACKEND_URL}/predict_delay", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Prediction Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Delay Probability", f"{result['delay_probability']*100:.1f}%")
                    with col2:
                        st.metric("Predicted Delay", f"{result['predicted_delay_minutes']} min")
                    with col3:
                        risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
                        st.metric("Risk Level", f"{risk_color[result['risk_level']]} {result['risk_level']}")
                    
                    st.subheader("📌 Contributing Factors")
                    for factor in result['factors']:
                        st.info(f"• {factor}")
                else:
                    st.error("Prediction failed")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Mode 3: Rerouting Engine
elif mode == "Rerouting Engine":
    st.header("🔄 Intelligent Rerouting System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        delayed_train = st.text_input("Delayed Train ID", "TR0041")
        current_station = st.text_input("Current Station", "Mumbai")
        delay_minutes = st.number_input("Delay (minutes)", min_value=0, max_value=180, value=30)
    
    with col2:
        destination = st.text_input("Destination Station", "Pune")
        available_routes = st.text_area("Available Routes (comma-separated)", "Route1,Route2")
    
    if st.button("🚀 Generate Rerouting Plan", type="primary"):
        with st.spinner("Computing optimal reroute..."):
            time.sleep(1)
            
            try:
                payload = {
                    "delayed_train_id": delayed_train,
                    "current_station": current_station,
                    "destination_station": destination,
                    "delay_minutes": delay_minutes,
                    "available_routes": [r.strip() for r in available_routes.split(",")]
                }
                
                response = requests.post(f"{BACKEND_URL}/reroute", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Rerouting Plan Generated!")
                    
                    # Recommended action
                    st.markdown(f"### 🎯 Recommended Action")
                    st.info(result['recommended_action'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Recovery Time", f"{result['estimated_recovery_time']} min")
                    with col2:
                        st.metric("Confidence Score", f"{result['confidence_score']*100:.0f}%")
                    
                    # Reroute path
                    st.markdown("### 🗺️ Suggested Route")
                    route_path = " → ".join(result['reroute_path'])
                    st.success(route_path)
                    
                    # Alternative trains
                    st.markdown("### 🚂 Alternative Trains")
                    for train in result['alternative_trains']:
                        st.markdown(f"""
                        <div class="rerouted-train">
                            🚆 <strong>{train['train_id']}</strong><br>
                            ⏰ Departure: {train['departure_time']}<br>
                            💺 Available Seats: {train['available_seats']}<br>
                            🛤️ Route: {train['route']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Decision buttons
                    st.markdown("### ✅ Dispatcher Decision")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ Accept Reroute", key="accept"):
                            st.success("Rerouting plan accepted!")
                    with col2:
                        if st.button("❌ Reject Reroute", key="reject"):
                            st.warning("Rerouting plan rejected!")
                    with col3:
                        if st.button("⏸️ Hold for Review", key="hold"):
                            st.info("Plan on hold for review")
                else:
                    st.error("Rerouting failed")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Mode 4: Upload Schedule
elif mode == "Upload Schedule":
    st.header("📤 Upload Train Schedule")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Uploaded {len(df)} train records")
        
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("📊 Analyze Schedule"):
            st.info("Schedule analysis coming soon...")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🚂 Smart Train Traffic Controller | Railway Automation System<br>
    Built with FastAPI, Streamlit & Docker | Hackathon Demo 2025
</div>
""", unsafe_allow_html=True)
