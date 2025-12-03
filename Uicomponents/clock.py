import time
import threading
import streamlit as st
from utils.spech import speak


# -----------------------------------------------------------
# SIDEBAR TIMER UI (Safe initialization inside)
# -----------------------------------------------------------
def sidebar_timer():
    # --- Initialize session state safely --------------------
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_remaining" not in st.session_state:
        st.session_state.timer_remaining = 0
    if "timer_finished" not in st.session_state:
        st.session_state.timer_finished = False

    # --- Sidebar UI ----------------------------------------
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

        if st.button("Start Timer"):
            if not st.session_state.timer_running:
                st.session_state.timer_running = True
                st.session_state.timer_remaining = duration

                # Start background timer thread
                t = threading.Thread(target=_run_timer, daemon=True)
                t.start()

        mins = st.session_state.timer_remaining // 60
        secs = st.session_state.timer_remaining % 60

        if st.session_state.timer_running:
            st.write(f"⏳ Time left: **{mins:02d}:{secs:02d}**")
        else:
            st.write(f"Ready: **{mins:02d}:{secs:02d}**")

        # Make the timer speak just once
        if st.session_state.timer_finished:
            speak("Timer is up. Take a break.")
            st.session_state.timer_finished = False


# -----------------------------------------------------------
# BACKGROUND THREAD
# Never crashes because we use .get() for safe reads
# -----------------------------------------------------------
def _run_timer():
    while True:
        time.sleep(1)

        running = st.session_state.get("timer_running", False)
        remaining = st.session_state.get("timer_remaining", 0)

        # If timer stopped externally or reset
        if not running:
            break

        if remaining > 0:
            st.session_state.timer_remaining = remaining - 1
        else:
            # Timer just finished
            st.session_state.timer_running = False
            st.session_state.timer_finished = True
            break
