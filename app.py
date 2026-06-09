
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.auth import register_user, login_user
from utils.placement import (
    save_progress,
    get_latest_progress,
    save_study_hours,
    get_total_study_hours
)
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="LearnTrack AI",
    page_icon="🎓",
    layout="centered"
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# AFTER LOGIN
# ==========================================

if st.session_state.logged_in:

    with st.sidebar:

        selected = option_menu(
            menu_title="LearnTrack AI",
            options=[
                "Dashboard",
                "Placement Tracker",
                "Study Planner",
                "Analytics",
                "Resources"
            ],
            icons=[
                "house",
                "graph-up",
                "book",
                "bar-chart",
                "collection"
            ],
            default_index=0
        )

    st.title(f"📊 {selected}")

    # ---------------- Dashboard ----------------

    if selected == "Dashboard":

        st.success(
            f"Welcome {st.session_state.username}"
        )

        data = get_latest_progress(
            st.session_state.username
        )
        total_hours = get_total_study_hours(
            st.session_state.username
        )

        if data:

            dsa_score = data[0]
            aptitude_score = data[1]
            project_score = data[2]
            interview_score = data[3]

            placement_score = int(
                (
                    dsa_score +
                    aptitude_score +
                    project_score +
                    interview_score
                ) / 4
            )

        else:

            dsa_score = 0
            placement_score = 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "DSA Progress",
            f"{dsa_score}%"
        )

        col2.metric(
            "Study Hours",
            f"{total_hours} hrs"
        )

        col3.metric(
            "Placement Score",
            f"{placement_score}%"
        )

        col4.metric(
            "Current Streak",
            f"{min(total_hours,30)} Days"
        )
    

    # ---------------- Placement Tracker ----------------

    elif selected == "Placement Tracker":

        st.subheader("Placement Progress Tracker")

        dsa = st.slider(
            "DSA Progress %",
            0,
            100,
            0
        )

        aptitude = st.slider(
            "Aptitude Progress %",
            0,
            100,
            0
        )

        projects = st.slider(
            "Projects Completion %",
            0,
            100,
            0
        )

        interviews = st.slider(
            "Interview Preparation %",
            0,
            100,
            0
        )

        if st.button("Save Progress"):

            save_progress(
                st.session_state.username,
                dsa,
                aptitude,
                projects,
                interviews
            )

            st.success(
                "Progress Saved Successfully"
            )

    # ---------------- Study Planner ----------------

    elif selected == "Study Planner":

        st.subheader(
            "AI Study Planner"
        )

        months = st.selectbox(
            "Placement Target",
            [
                "3 Months",
                "6 Months",
                "12 Months"
            ]
        )

        if st.button("Generate Roadmap"):

            if months == "3 Months":

                st.markdown("""
### Month 1
- Arrays
- Strings
- Linked List

### Month 2
- Stack
- Queue
- Trees

### Month 3
- Graphs
- DBMS
- Aptitude
                """)
                

            elif months == "6 Months":

                st.markdown("""
### Month 1
- Arrays
- Strings

### Month 2
- Linked List
- Stack
- Queue

### Month 3
- Trees
- Graphs

### Month 4
- DBMS
- OS

### Month 5
- OOP
- Aptitude

### Month 6
- Mock Interviews
- Projects
                """)

            else:

                st.markdown("""
### Months 1-3
- Complete DSA Basics

### Months 4-6
- Advanced DSA

### Months 7-9
- Core Subjects

### Months 10-12
- Projects
- Interviews
- Placement Preparation
                """)
        st.divider()

    st.subheader("Daily Study Hours")

    hours = st.number_input(
        "Hours Studied Today",
        min_value=0,
        max_value=24,
        value=1
    )

    if st.button("Save Study Hours"):

        save_study_hours(
            st.session_state.username,
            hours
        )

        st.success(
            "Study Hours Saved"
        )

    # ---------------- Analytics ----------------

    elif selected == "Analytics":

        data = get_latest_progress(
            st.session_state.username
        )

        if data:

            df = pd.DataFrame(
                {
                    "Category": [
                        "DSA",
                        "Aptitude",
                        "Projects",
                        "Interviews"
                    ],
                    "Progress": [
                        data[0],
                        data[1],
                        data[2],
                        data[3]
                    ]
                }
            )

            fig = px.bar(
                df,
                x="Category",
                y="Progress",
                title="Placement Readiness"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No Data Available"
            )

    # ---------------- Resources ----------------

    elif selected == "Resources":

        st.subheader("Learning Resources")

        st.link_button(
            "Striver DSA Sheet",
            "https://takeuforward.org"
        )

        st.link_button(
            "GeeksforGeeks",
            "https://www.geeksforgeeks.org"
        )

        st.link_button(
            "LeetCode",
            "https://leetcode.com"
        )

        st.link_button(
            "InterviewBit",
            "https://www.interviewbit.com"
        )

    # ---------------- Logout ----------------

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    st.stop()

# ==========================================
# LOGIN / REGISTER
# ==========================================

st.title("🎓 LearnTrack AI")
st.markdown(
    "### Smart Placement Preparation Platform"
)

tab1, tab2 = st.tabs(
    ["🔐 Login", "📝 Register"]
)

# Login

with tab1:

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button("Login"):

        authenticated = login_user(
            username,
            password
        )

        if authenticated:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

# Register

with tab2:

    new_user = st.text_input(
        "New Username"
    )

    new_pass = st.text_input(
        "New Password",
        type="password"
    )

    if st.button("Register"):

        if new_user == "" or new_pass == "":

            st.error(
                "Please fill all fields"
            )

        else:

            success = register_user(
                new_user,
                new_pass
            )

            if success:

                st.success(
                    "Account Created Successfully"
                )

            else:

                st.error(
                    "Username Already Exists"
                )
