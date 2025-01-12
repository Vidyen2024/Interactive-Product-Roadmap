import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive Product Roadmap 📅", layout="wide", page_icon="📅")

# Initialize or load task data
if "tasks" not in st.session_state:
    st.session_state["tasks"] = pd.DataFrame(columns=["Task", "Priority", "Status", "Due Date"])

# Sidebar: Add or Edit Task
st.sidebar.header("Manage Tasks")
with st.sidebar.form("task_form"):
    task_name = st.text_input("Task Name")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    status = st.selectbox("Status", ["Backlog", "In Progress", "Completed"])
    due_date = st.date_input("Due Date", datetime.today() + timedelta(days=7))
    submit_button = st.form_submit_button("Add Task")

    if submit_button:
        if task_name.strip():  # Ensure task name is not empty or just spaces
            new_task = {
                "Task": task_name.strip(),
                "Priority": priority,
                "Status": status,
                "Due Date": due_date,
            }
            st.session_state["tasks"] = pd.concat(
                [st.session_state["tasks"], pd.DataFrame([new_task])],
                ignore_index=True,
            )
            st.success(f"Task '{task_name}' added successfully!")
        else:
            st.error("Task name cannot be empty.")

# Main Dashboard
st.title("Interactive Product Roadmap 📅")
st.write("Easily manage and visualize your product roadmap.")

# Filters
st.subheader("Filters")
search_keyword = st.text_input("Search Tasks (by name)")
priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
status_filter = st.selectbox("Filter by Status", ["All", "Backlog", "In Progress", "Completed"])

# Apply Filters
filtered_tasks = st.session_state["tasks"]
if search_keyword:
    filtered_tasks = filtered_tasks[
        filtered_tasks["Task"].str.contains(search_keyword, case=False)
    ]
if priority_filter != "All":
    filtered_tasks = filtered_tasks[filtered_tasks["Priority"] == priority_filter]
if status_filter != "All":
    filtered_tasks = filtered_tasks[filtered_tasks["Status"] == status_filter]

# Display Task Table
st.subheader("Roadmap Table")
if not filtered_tasks.empty:
    st.dataframe(filtered_tasks.style.format({"Due Date": lambda x: x.strftime("%Y-%m-%d")}))
else:
    st.warning("No tasks match the current filters. Add a task or adjust the filters.")

# Gantt Chart
st.subheader("Gantt Chart")
if not filtered_tasks.empty:
    gantt_chart = px.timeline(
        filtered_tasks,
        x_start="Due Date",
        x_end="Due Date",
        y="Task",
        color="Priority",
        title="Roadmap Gantt Chart",
        labels={"Due Date": "Due Date", "Task": "Task Name"},
    )
    gantt_chart.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(gantt_chart, use_container_width=True)
else:
    st.info("Add tasks to visualize them on the Gantt chart.")

# Download Roadmap as CSV
st.markdown("### Export Roadmap")
if not st.session_state["tasks"].empty:
    csv = st.session_state["tasks"].to_csv(index=False)
    st.download_button(
        label="Download Roadmap as CSV",
        data=csv,
        file_name="roadmap.csv",
        mime="text/csv",
    )