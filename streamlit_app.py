import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Period durations for the 14-day simulation
period_durations = {
    1: timedelta(days=1, hours=7, minutes=22),
    2: timedelta(hours=20, minutes=54),
    3: timedelta(hours=20, minutes=54),
    4: timedelta(days=4, hours=18, minutes=59),
    5: timedelta(days=5, hours=5, minutes=24)
}

# Alert schedule
alert_schedule = [
    {"label": "5 days before", "delta": timedelta(hours=4, minutes=29), "color": "🟡 Yellow", "flashes": 1},
    {"label": "1 day before", "delta": timedelta(hours=1, minutes=29), "color": "🟡 Yellow", "flashes": 2},
    {"label": "Due date", "delta": timedelta(hours=1), "color": "🟢 Green", "flashes": 2},
    {"label": "Past due", "delta": timedelta(minutes=-3, seconds=-44), "color": "🔴 Red", "flashes": 1}
]

# Streamlit UI
st.set_page_config(page_title="14-Day Alert Time Scheduler", layout="centered")
st.title("📟 14-Day Device Alert Time Viewer")
st.markdown("Input the **device configuration time** and **period (1-5)** to view alert blink schedule.")

# Input section
config_time_str = st.text_input("Configuration Time (YYYY-MM-DD HH:MM:SS)", value="2025-07-29 10:00:00")
period = st.selectbox("Period Number", options=[1, 2, 3, 4, 5])

# Compute and display results
if st.button("Show Alert Times"):
    try:
        config_time = datetime.strptime(config_time_str, "%Y-%m-%d %H:%M:%S")
        duration = period_durations[period]
        end_time = config_time + duration

        alerts = []
        for alert in alert_schedule:
            alert_time = end_time - alert["delta"]
            alerts.append({
                "Alert Stage": alert["label"],
                "Time": alert_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Flashes": alert["flashes"],
                "Color": alert["color"]
            })

        df = pd.DataFrame(alerts)
        st.subheader("📅 Expected Alert Times")
        st.dataframe(df, use_container_width=True)

        st.success("Alert schedule displayed successfully.")

    except ValueError:
        st.error("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS")
