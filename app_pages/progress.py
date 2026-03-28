import streamlit as st
from course_data import MODULES, TOTAL_LESSONS, TOTAL_DURATION

completed_lessons = {k for k, v in st.session_state.lesson_progress.items() if v == "completed"}
pct_complete = round(len(completed_lessons) / TOTAL_LESSONS * 100) if TOTAL_LESSONS > 0 else 0
completed_duration = sum(
    l["duration_min"]
    for m in MODULES
    for l in m["lessons"]
    if l["id"] in completed_lessons
)

with st.container(horizontal=True):
    st.metric(f"{pct_complete}%", "course complete", border=True)
    st.metric(f"{len(completed_lessons)} of {TOTAL_LESSONS}", "lessons done", border=True)
    st.metric(f"{completed_duration} min", "time invested", border=True)
    st.metric(f"~{TOTAL_DURATION - completed_duration} min", "remaining", border=True)

st.subheader("Module progress")

for m in MODULES:
    lesson_ids = {l["id"] for l in m["lessons"]}
    done = len(lesson_ids.intersection(completed_lessons))
    total = len(m["lessons"])
    pct = round(done / total * 100) if total > 0 else 0
    st.progress(pct / 100, text=f"Module {m['id']}: {m['title']} \u2014 {done}/{total} lessons")

st.subheader("Lesson completion")

for m in MODULES:
    with st.expander(f"Module {m['id']}: {m['title']}"):
        for l in m["lessons"]:
            is_done = l["id"] in completed_lessons
            icon = ":material/check_circle:" if is_done else ":material/radio_button_unchecked:"
            status = "Complete" if is_done else "Not started"
            st.markdown(f"{icon} **{l['title']}** ({l['duration_min']} min) \u2014 {status}")

if st.session_state.get("in_sis") and st.session_state.get("snowpark_session"):
    st.subheader("My SnowWork usage (live data)")
    try:
        session = st.session_state.snowpark_session
        user_result = session.sql("SELECT CURRENT_USER()").collect()
        current_user = user_result[0][0]

        usage_df = session.sql(f"""
            SELECT
                USAGE_DATE,
                TOOL_NAME,
                SUM(TOTAL_PROMPTS) AS PROMPTS
            FROM SNOW_CERTIFIED.EMPLOYEE.AGG_DAILY_EMPLOYEE_AI_USAGE
            WHERE LDAP = '{current_user}'
              AND USAGE_DATE >= DATEADD('day', -30, CURRENT_DATE())
            GROUP BY USAGE_DATE, TOOL_NAME
            ORDER BY USAGE_DATE
        """).to_pandas()

        if not usage_df.empty:
            st.line_chart(usage_df, x="USAGE_DATE", y="PROMPTS", color="TOOL_NAME")
        else:
            st.caption("No SnowWork usage data found for the last 30 days.")
    except Exception as e:
        st.caption(f"Usage data unavailable: {e}")
else:
    st.caption("SnowWork usage data is available when running in Snowflake (Snowsight).")
