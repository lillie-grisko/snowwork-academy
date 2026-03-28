import streamlit as st
from course_data import MODULES


def find_lesson(module_id, lesson_id):
    for m in MODULES:
        if m["id"] == module_id:
            for l in m["lessons"]:
                if l["id"] == lesson_id:
                    return m, l
    return MODULES[0], MODULES[0]["lessons"][0]


mod_id, les_id = st.session_state.current_lesson
module, lesson = find_lesson(mod_id, les_id)

all_lessons = []
for m in MODULES:
    for l in m["lessons"]:
        all_lessons.append((m, l))

current_idx = next(i for i, (m, l) in enumerate(all_lessons) if l["id"] == lesson["id"])

st.html(f"""
<div style="
    background: linear-gradient(135deg, #29B5E8 0%, #1B6B9A 100%);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
">
    <p style="color: rgba(255,255,255,0.75); margin: 0 0 0.25rem 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">
        Module {module['id']}: {module['title']}
    </p>
    <h2 style="color: white; margin: 0; font-size: 1.6rem; font-weight: 600;">
        {lesson['title']}
    </h2>
</div>
""")

st.progress((current_idx + 1) / len(all_lessons), text=f"Lesson {current_idx + 1} of {len(all_lessons)}")

with st.container(border=True):
    st.markdown(f"##### :material/format_quote: The Hook")
    st.markdown(f"*{lesson['hook']}*")

st.markdown("##### :material/menu_book: Key Concepts")

for title, body in lesson["content"]:
    with st.expander(f"**{title}**", expanded=False):
        st.markdown(body)

if lesson.get("pro_tip"):
    st.info(f"**Pro tip:** {lesson['pro_tip']}", icon=":material/tips_and_updates:")

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if current_idx > 0:
        if st.button("Previous", icon=":material/arrow_back:", use_container_width=True):
            prev_mod, prev_les = all_lessons[current_idx - 1]
            st.session_state.current_lesson = (prev_mod["id"], prev_les["id"])
            st.rerun()

with col2:
    is_complete = st.session_state.lesson_progress.get(lesson["id"]) == "completed"
    if is_complete:
        st.success("Lesson complete", icon=":material/check_circle:")
    else:
        if st.button("Mark complete & continue", icon=":material/check:", type="primary", use_container_width=True):
            st.session_state.lesson_progress[lesson["id"]] = "completed"
            if current_idx < len(all_lessons) - 1:
                next_mod, next_les = all_lessons[current_idx + 1]
                st.session_state.current_lesson = (next_mod["id"], next_les["id"])
            st.rerun()

with col3:
    if current_idx < len(all_lessons) - 1:
        if st.button("Next", icon=":material/arrow_forward:", use_container_width=True):
            next_mod, next_les = all_lessons[current_idx + 1]
            st.session_state.current_lesson = (next_mod["id"], next_les["id"])
            st.rerun()
