import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.io as pio

# Display Title and Description
st.title("Employee Engagement Dashboard")
st.markdown("Welcome to this month's Engagement Dashboard.")

conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
existing_data = conn.read(worksheet="Surveys", usecols=list(range(5)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Display existing data as a table
st.subheader("Existing Dashboard Data")
st.dataframe(existing_data)

# Add a new element with a button
if st.button("Add New Element"):
    new_element = st.text_input("Enter New Element:")

    if new_element:
        updated_data = existing_data.append({"Element": new_element}, ignore_index=True)
        conn.update(worksheet="DashboardData", data=updated_data)
        st.success("New element added successfully!")

# Visualization type dropdown
visualization_type_options = ["Select Visualization Type", "Table", "Bar Chart", "Pie Chart", "Line Chart"]
visualization_type = st.selectbox("Select Data Visualization Type", visualization_type_options)

# Display the selected visualization type
st.write(f"Selected Data Visualization Type: {visualization_type}")

# Dropdown for selecting columns
selected_columns = st.multiselect("Select Columns", existing_data.columns)

# Initialize fig variable
fig = None

# Display visualization based on the selected type
if visualization_type == "Table":
    # Display table for the selected columns
    st.dataframe(existing_data[selected_columns])

elif visualization_type == "Bar Chart":
    # Display bar chart
    fig = px.bar(existing_data, x=existing_data.index, y=selected_columns, title=f"{visualization_type} Chart")
    st.plotly_chart(fig)

elif visualization_type == "Pie Chart":
    # Display pie chart
    fig = px.pie(existing_data, names=selected_columns, title=f"{visualization_type} Chart")
    st.plotly_chart(fig)

elif visualization_type == "Line Chart":
    # Display line chart using Altair
    data = existing_data[selected_columns]
    chart = alt.Chart(data).mark_line().encode(
        x=data.index,
        y=selected_columns,
        color=alt.Color(selected_columns, legend=alt.Legend(title="Columns")),
    ).properties(
        title=f"{visualization_type} Chart",
        width=600,
        height=400,
    )
    st.altair_chart(chart)

# Download button for the chart as an image
if fig is not None:
    # Save the plotly figure as an image file
    image_data = pio.to_image(fig, format="png")

    # Display the download button
    st.download_button(
        label="Download Chart as Image",
        data=image_data,
        file_name=f"{visualization_type}_chart.png",
        key=f"{visualization_type}_chart",
    )
