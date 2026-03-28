import streamlit as st
from course_data import MODULES, TOTAL_LESSONS, TOTAL_DURATION


def get_completed_lessons():
    return {k for k, v in st.session_state.lesson_progress.items() if v == "completed"}


def get_completed_modules():
    completed = get_completed_lessons()
    done = []
    for m in MODULES:
        lesson_ids = {l["id"] for l in m["lessons"]}
        if lesson_ids.issubset(completed):
            done.append(m["id"])
    return done


completed_lessons = get_completed_lessons()
completed_modules = get_completed_modules()
pct_complete = round(len(completed_lessons) / TOTAL_LESSONS * 100) if TOTAL_LESSONS > 0 else 0

st.html("""
<div style="
    background: linear-gradient(135deg, #29B5E8 0%, #1B6B9A 100%);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    margin-bottom: 1rem;
">
    <h1 style="color: white; margin: 0 0 0.5rem 0; font-size: 2.2rem; font-weight: 700;">
        SnowWork Academy
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 1.05rem; line-height: 1.6; max-width: 700px;">
        Master SnowWork (Project Falcon) &mdash; Snowflake's autonomous AI platform &mdash; and turn your daily selling workflows into automated, data-driven actions.
    </p>
</div>
""")

with st.container(border=True):
    st.markdown("##### :material/school: Learning Objectives")
    st.markdown("""
- **Explain** what SnowWork is and how it differs from CoCo, Intelligence, and Raven — *Sales Tooling Fluency*
- **Execute** account research, prospect briefs, and consumption analysis using SnowWork skills — *Account Intelligence & Territory Planning*
- **Prepare** for customer meetings in under 10 minutes using a repeatable SnowWork workflow — *Meeting Preparation & MEDDPICC+ Qualification*
- **Analyze** pipeline health, deal hygiene, and expansion signals with SnowWork intelligence skills — *Pipeline Management & Forecasting*
- **Create** custom skills tailored to your personal selling rhythm and territory — *Time Management & Operating Rhythm*
- **Choose** the right AI tool for any task using the SnowWork decision framework — *Sales Process Execution*
""")

st.space("small")

with st.container(horizontal=True):
    st.metric(
        f"{len(completed_modules)} of {len(MODULES)}",
        "Modules Complete",
        border=True,
    )
    st.metric(
        f"{len(completed_lessons)} of {TOTAL_LESSONS}",
        "Lessons Complete",
        border=True,
    )
    st.metric(
        f"{pct_complete}%",
        "Course Progress",
        border=True,
    )
    st.metric(
        f"~{TOTAL_DURATION} min",
        "Total Course Time",
        border=True,
    )

next_lesson = None
next_module = None
for m in MODULES:
    for l in m["lessons"]:
        if l["id"] not in completed_lessons:
            next_lesson = l
            next_module = m
            break
    if next_lesson:
        break

if next_lesson:
    with st.container(border=True):
        col1, col2 = st.columns([4, 1], vertical_alignment="center")
        with col1:
            st.markdown(f"##### :material/play_circle: Continue Learning")
            st.caption(f"Module {next_module['id']}: {next_module['title']} — Lesson: {next_lesson['title']}")
        with col2:
            if st.button("Resume", icon=":material/play_arrow:", type="primary", use_container_width=True):
                st.session_state.current_lesson = (next_module["id"], next_lesson["id"])
                st.switch_page("app_pages/learn.py")
else:
    st.success("You've completed all lessons!", icon=":material/celebration:")

st.markdown("##### :material/view_module: Modules")

row1 = st.columns(3)
row2 = st.columns(3)
all_cols = row1 + row2

for i, m in enumerate(MODULES):
    if i >= len(all_cols):
        break
    with all_cols[i]:
        with st.container(border=True):
            lesson_ids = {l["id"] for l in m["lessons"]}
            done_count = len(lesson_ids.intersection(completed_lessons))
            total_count = len(m["lessons"])
            is_complete = m["id"] in completed_modules

            if is_complete:
                st.badge("Complete", icon=":material/check_circle:", color="green")
            elif done_count > 0:
                st.badge(f"{done_count}/{total_count}", icon=":material/pending:", color="orange")
            else:
                prev_complete = (m["id"] == 1) or ((m["id"] - 1) in completed_modules)
                if prev_complete:
                    st.badge("Ready", icon=":material/play_circle:", color="blue")
                else:
                    st.badge("Locked", color="gray")

            st.markdown(f"**{m['icon']} {m['title']}**")
            st.caption(f"{m['duration_min']} min  ·  {total_count} lesson{'s' if total_count > 1 else ''}")
            st.caption(m["description"])

            if st.button("Start", key=f"open_mod_{m['id']}", use_container_width=True, type="primary"):
                first_lesson = m["lessons"][0]
                st.session_state.current_lesson = (m["id"], first_lesson["id"])
                st.switch_page("app_pages/learn.py")
