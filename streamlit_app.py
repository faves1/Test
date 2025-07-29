import streamlit as st
from datetime import datetime, timedelta

# Period durations
period_durations = {
    "Period 1": timedelta(days=1, hours=7, minutes=22),
    "Period 2": timedelta(hours=20, minutes=54),
    "Period 3": timedelta(hours=20, minutes=54),
    "Period 5": timedelta(days=5, hours=5, minutes=24),
}

# Alert Offsets
yellow1_offset = timedelta(hours=4, minutes=29)
yellow2_offset = timedelta(hours=1, minutes=29)
green_offset = timedelta(seconds=0)
red_offset = timedelta(seconds=1)

# UI
# Streamlit UI
st.set_page_config(page_title="14-Day Alert Time Scheduler", layout="centered")
st.title("📟 14-Day Device Alert Time Viewer")
st.markdown("Input the **device configuration time** and **period (1-5)** to view alert blink schedule.")

selected_period = st.selectbox("Select a Monitoring Period", list(period_durations.keys()))

# Combine date and time inputs
date_input = st.date_input("📅 Select Configuration Date", datetime.now().date())
time_input = st.time_input("🕒 Select Configuration Time", datetime.now().time())
config_time = datetime.combine(date_input, time_input)

if st.button("🔔 Show Alert Times"):
    period_duration = period_durations[selected_period]
    due_time = config_time + period_duration

    # Alert timestamps
    yellow1_time = due_time - yellow1_offset
    yellow2_time = due_time - yellow2_offset
    green_time = due_time
    red_time = due_time + red_offset

    # Display Results
    st.markdown("### 🕒 Alert Schedule")
    st.info(f"**Due Time:** {due_time.strftime('%Y-%m-%d %H:%M:%S')}")

    st.warning(f"🟡 Yellow Alert 1 (1 flash at -4h29m): {yellow1_time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.warning(f"🟡 Yellow Alert 2 (2 flashes at -1h29m): {yellow2_time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.success(f"🟢 Green Alert (2 flashes at due time): {green_time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.error(f"🔴 Red Alert (1 flash after due time): {red_time.strftime('%Y-%m-%d %H:%M:%S')}")
