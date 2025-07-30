import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO

# Period durations
period_durations = {
    "Period 1": timedelta(days=1, hours=7, minutes=22),
    "Period 2": timedelta(hours=20, minutes=54),
    "Period 3": timedelta(hours=20, minutes=54),
    "Period 4": timedelta(days=4, hours=18, minutes=59),
    "Period 5": timedelta(days=5, hours=5, minutes=24),
}

# Alert Offsets
yellow1_offset = timedelta(hours=4, minutes=29)
yellow2_offset = timedelta(hours=1, minutes=29)
green_offset = timedelta(seconds=0)
red_offset = timedelta(seconds=1)

# Initialize session state
if "alert_data" not in st.session_state:
    st.session_state.alert_data = []

# UI
# Streamlit UI
st.set_page_config(page_title="14-Day Alert Time Scheduler", layout="centered")
st.title("📟 14-Day Device Alert Time Viewer")
st.markdown("Input the **device configuration time** and **period (1-5)** to view alert blink schedule.")

user_name = st.text_input("Enter User's Name")
device_name = st.text_input("🆔 Enter Device ID")
selected_period = st.selectbox("Select a Monitoring Period", list(period_durations.keys()))

manual_input = st.text_input(
    "📝 Enter Configuration Time (Format: YYYY-MM-DD HH:MM)",
    value=datetime.now().strftime('%Y-%m-%d %H:%M')
)

if st.button("➕ Add to Table"):
    try:
        config_time = datetime.strptime(manual_input, "%Y-%m-%d %H:%M")
        period_duration = period_durations[selected_period]
        due_time = config_time + period_duration

        # Alert times
        yellow1_time = due_time - yellow1_offset
        yellow2_time = due_time - yellow2_offset
        green_time = due_time
        red_time = due_time + red_offset

        # Add entry to session_state
        st.session_state.alert_data.append({
            "User Name": user_name,
            "Device ID": device_name,
            "Configuration Time": config_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Period": selected_period,
            "Due Time": due_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Yellow Alert 1 (−4h29m)": yellow1_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Yellow Alert 2 (−1h29m)": yellow2_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Green Alert (Due Time)": green_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Red Alert (After Due Time)": red_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        st.success("✅ Entry added to table.")

    except ValueError:
        st.error("❌ Please enter a valid datetime in format: YYYY-MM-DD HH:MM")

# Display table
if st.session_state.alert_data:
    df = pd.DataFrame(st.session_state.alert_data)
    st.dataframe(df)

    # Download to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Alert Schedule')
    output.seek(0)

    st.download_button(
        label="📥 Download Full Table as Excel",
        data=output,
        file_name="full_alert_schedule.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
