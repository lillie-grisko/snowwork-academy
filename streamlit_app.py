import streamlit as st

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    IN_SIS = True
except Exception:
    IN_SIS = False
    session = None

if "lesson_progress" not in st.session_state:
    st.session_state.lesson_progress = {}
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = (1, 1)

st.session_state.snowpark_session = session
st.session_state.in_sis = IN_SIS

page = st.navigation([
    st.Page("app_pages/home.py", title="Home", icon=":material/rocket_launch:"),
    st.Page("app_pages/learn.py", title="Learn", icon=":material/menu_book:"),
    st.Page("app_pages/tools.py", title="Which tool?", icon=":material/handyman:"),
    st.Page("app_pages/prompts.py", title="Prompt library", icon=":material/chat:"),
    st.Page("app_pages/progress.py", title="My progress", icon=":material/trending_up:"),
], position="top")

page.run()
