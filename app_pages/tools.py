import streamlit as st
from course_data import TOOL_DATA

st.html("""
<div style="
    background: linear-gradient(135deg, #29B5E8 0%, #1B6B9A 100%);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
">
    <h2 style="color: white; margin: 0 0 0.25rem 0; font-size: 1.6rem; font-weight: 600;">
        Which Tool Should I Use?
    </h2>
    <p style="color: rgba(255,255,255,0.85); margin: 0; font-size: 0.95rem;">
        Select a task to get the right tool recommendation.
    </p>
</div>
""")

task_options = [
    "Account research",
    "Meeting prep",
    "Pipeline management",
    "Customer comms",
    "Competitive intel",
    "Executive briefs",
    "Quick lookup",
    "Customer demo",
]

selected_task = st.segmented_control("What are you trying to do?", task_options, default="Account research")

matching_tools = []
for tool in TOOL_DATA:
    relevance = 0
    if selected_task in tool["tasks"]:
        relevance = 3
    elif any(selected_task.lower() in t.lower() for t in tool["tasks"]):
        relevance = 2
    if relevance > 0:
        matching_tools.append((tool, relevance))

matching_tools.sort(key=lambda x: x[1], reverse=True)

if matching_tools:
    best_tool = matching_tools[0][0]

    with st.container(border=True):
        st.markdown(f"### {best_tool['icon']} Recommended: **{best_tool['name']}**")
        st.markdown(f"**Why:** {best_tool['best_for']}")
        st.markdown(f"**Example:** {best_tool['example']}")
        st.badge(best_tool["audience"], color="blue")

    if len(matching_tools) > 1:
        st.markdown("##### Also Consider")
        for tool, _ in matching_tools[1:]:
            with st.container(border=True):
                st.markdown(f"{tool['icon']} **{tool['name']}** — {tool['best_for']}")

    not_recommended = [t for t in TOOL_DATA if t["name"] != best_tool["name"] and t not in [x[0] for x in matching_tools]]
    if not_recommended:
        with st.expander("Why not the others?"):
            for tool in not_recommended:
                st.markdown(f"- **{tool['name']}:** {tool['best_for']} *(not ideal for {selected_task.lower()})*")

else:
    st.info("Select a task above to get a tool recommendation.", icon=":material/info:")

st.divider()

with st.expander("Full Tool Comparison", icon=":material/compare:"):
    import pandas as pd

    df = pd.DataFrame([
        {
            "Tool": t["name"],
            "Best For": t["best_for"],
            "Audience": t["audience"],
            "Depth": t["depth"],
        }
        for t in TOOL_DATA
    ])
    st.dataframe(df, hide_index=True, use_container_width=True)
