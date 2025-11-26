import time
import threading
import streamlit as st
from utils.spech import speak

def sidebar_timer():
    with st.sidebar:
        st.header("⏲️ Quick Timer")

        preset = st.selectbox(
            "Select Duration",
            ["20 minutes", "30 minutes", "1 hour"]
        )

        duration = {
            "20 minutes": 20 * 60,
            "30 minutes": 30 * 60,
            "1 hour": 60 * 60
        }[preset]

        # session states
        if "timer_running" not in st.session_state:
            st.session_state.timer_running = False
        if "timer_remaining" not in st.session_state:
            st.session_state.timer_remaining = duration

        if st.button("Start Timer"):
            if not st.session_state.timer_running:
                st.session_state.timer_running = True
                st.session_state.timer_remaining = duration
                threading.Thread(target=_run_timer, daemon=True).start()

        # UI display (non-blocking)
        mins = st.session_state.timer_remaining // 60
        secs = st.session_state.timer_remaining % 60

        if st.session_state.timer_running:
            st.write(f"⏳ Time left: **{mins:02d}:{secs:02d}**")
        else:
            st.write(f"Ready: **{mins:02d}:{secs:02d}**")


def _run_timer():
    """Runs inside background thread — safe, no freezing."""
    while st.session_state.timer_running and st.session_state.timer_remaining > 0:
        time.sleep(1)
        st.session_state.timer_remaining -= 1

    if st.session_state.timer_running:
        st.session_state.timer_running = False
        speak("⏲️ Timer is up. Take a break.")
