import streamlit as st
from course_data import PROMPT_LIBRARY

categories = sorted(set(p["category"] for p in PROMPT_LIBRARY))
selected_cats = st.pills("Filter by workflow", categories, selection_mode="multi", default=None)

search = st.text_input("Search prompts", placeholder="e.g. account summary, pipeline, competitive...")

filtered = PROMPT_LIBRARY
if selected_cats:
    filtered = [p for p in filtered if p["category"] in selected_cats]
if search:
    search_lower = search.lower()
    filtered = [
        p
        for p in filtered
        if search_lower in p["prompt"].lower()
        or search_lower in p["description"].lower()
        or search_lower in p["category"].lower()
    ]

st.caption(f"Showing {len(filtered)} prompt{'s' if len(filtered) != 1 else ''}")

for p in filtered:
    with st.container(border=True):
        col1, col2 = st.columns([4, 1], vertical_alignment="center")
        with col1:
            st.markdown(f"**{p['category']}**")
            st.code(p["prompt"], language=None)
            st.caption(p["description"])
        with col2:
            tool_colors = {
                "SnowWork": "green",
                "Cortex Code (CoCo)": "blue",
                "Raven": "orange",
                "Snowflake Intelligence": "red",
            }
            st.badge(p["tool"], color=tool_colors.get(p["tool"], "gray"))

if not filtered:
    st.info("No prompts match your filters. Try broadening your search.", icon=":material/search_off:")
