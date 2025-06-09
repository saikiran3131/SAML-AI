import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import plotly.express as px
import json

# Page config
st.set_page_config(page_title="Streamlit Component Showcase", layout="wide")

# Title and headers
st.title("🌟 Streamlit Component Showcase")
st.header("1. Basic Text and Formatting")
st.subheader("Subheaders and Markdown")
st.markdown("**Bold**, _italic_, `code`, and [link](https://streamlit.io)")
st.caption("This is a caption")
st.divider()

# Input Widgets
st.header("2. Input Widgets")
name = st.text_input("What's your name?")
bio = st.text_area("Tell us about yourself:")
age = st.number_input("Age", min_value=1, max_value=100)
dob = st.date_input("Date of Birth")
appointment = st.time_input("Preferred time")
gender = st.radio("Gender", ["Male", "Female", "Other"])
skills = st.multiselect("Select your skills", ["Python", "ML", "DS", "Web"])
score = st.slider("Your satisfaction score", 0, 100, 50)
agree = st.checkbox("I agree to the terms")
submit = st.button("Submit")

if submit:
    st.success(f"Hello, {name}! You're {age} years old. ✅")

st.divider()

# Sidebar Example
st.sidebar.title("Sidebar Controls")
sidebar_val = st.sidebar.selectbox("Choose a color", ["Red", "Green", "Blue"])

# File uploader and download
st.header("3. File Upload and Download")
uploaded_file = st.file_uploader("Upload a CSV")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    st.download_button("Download this CSV", uploaded_file.read(), file_name="download.csv")

st.divider()

# Media
st.header("4. Media Display")
st.image("https://placekitten.com/400/300", caption="A cute kitten 🐱")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
st.video("https://www.youtube.com/watch?v=5qap5aO4i9A")

st.divider()

# Data Display
st.header("5. Data Display")
data = pd.DataFrame({
    "Category": ["A", "B", "C"],
    "Values": [100, 200, 300]
})
st.table(data)
st.json(json.dumps({"name": name, "skills": skills}))
st.metric(label="Growth", value="120%", delta="+20%")

st.divider()

# Charts and Plots
st.header("6. Charts and Plots")

# Line chart
st.subheader("Line Chart")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
st.line_chart(chart_data)

# Matplotlib
st.subheader("Matplotlib Plot")
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
st.pyplot(fig)

# Plotly
st.subheader("Plotly Chart")
plot_data = px.data.iris()
fig_plotly = px.scatter(plot_data, x="sepal_width", y="sepal_length", color="species")
st.plotly_chart(fig_plotly)

st.divider()

# Layout: columns, tabs, expander
st.header("7. Layouts: Columns, Tabs, Expander")
col1, col2 = st.columns(2)
col1.write("Column 1")
col2.write("Column 2")

with st.expander("Click to Expand"):
    st.write("This is hidden unless expanded.")

tab1, tab2 = st.tabs(["📊 Chart", "📄 Info"])
with tab1:
    st.write("Charts go here!")
with tab2:
    st.write("Details and documentation.")

st.divider()

# Session State and Forms
st.header("8. Session State and Forms")
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment Counter"):
    st.session_state.counter += 1

st.write(f"Counter value: {st.session_state.counter}")

# Form Example
with st.form("my_form"):
    name_form = st.text_input("Enter name in form")
    submitted = st.form_submit_button("Submit Form")
    if submitted:
        st.success(f"Form submitted for: {name_form}")

st.divider()

# Progress, Spinner, Toast
st.header("9. Progress, Spinner and Notifications")
progress = st.progress(0)
for i in range(1, 101):
    time.sleep(0.01)
    progress.progress(i)

with st.spinner("Processing..."):
    time.sleep(2)
st.success("Done!")

st.toast("Here's a toast message! 🔔")

# Query Params (Experimental)
params = st.experimental_get_query_params()
st.write("Current query params:", params)

# Cache
@st.cache_data
def expensive_computation(x):
    time.sleep(2)
    return x * 10

result = expensive_computation(5)
st.write("Cached result:", result)

