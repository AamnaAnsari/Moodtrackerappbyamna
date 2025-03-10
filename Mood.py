import streamlit as st  # For creating web interface
import pandas as pd  # For data manipulation
import datetime  # For handling dates
import csv  # For reading and writing CSV file
import os  # For file operations

# Define the file name for storing mood data
MOOD_FILE = "mood_tracker.csv"

# Ensure the CSV file has correct headers
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Mood"])  # ✅ Fix: Ensure headers are correct

# Function to read mood data from the CSV file
def load_mood_data():
    if os.path.exists(MOOD_FILE):
        try:
            df = pd.read_csv(MOOD_FILE, encoding="utf-8")
            if "Date" not in df.columns or "Mood" not in df.columns:
                st.error("⚠️ CSV file has incorrect columns! Resetting file...")
                return pd.DataFrame(columns=["Date", "Mood"])
            return df
        except Exception as e:
            st.error(f"⚠️ Error loading data: {e}")
            return pd.DataFrame(columns=["Date", "Mood"])
    return pd.DataFrame(columns=["Date", "Mood"])

# Function to add new mood entry to CSV file
def save_mood_data(date, mood):
    with open(MOOD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, mood])

# Streamlit app title with custom styling
st.set_page_config(page_title="Mood Tracker", page_icon="😊", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #f4f4f4;}
        .stApp {background-color: #ffffff; padding: 20px;}
        .stButton>button {background-color: #ffcc00; color: black; font-size: 16px; border-radius: 10px; padding: 10px 20px;}
    </style>
    """, unsafe_allow_html=True)

st.title("😊 Mood Tracker")
st.markdown("Track your daily emotions and visualize your mood trends! 💡")

# Get today's date
today = datetime.date.today()

# Mood options with emojis
mood_options = ["😃 Happy", "😢 Sad", "😡 Angry", "😐 Neutral", "🤩 Excited", "🥱 Tired", "😔 Depressed", "😎 Confident", "😨 Anxious", "😤 Frustrated"]

# Layout for input section
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("How are you feeling today?")
    mood = st.selectbox("Select your mood", mood_options)

with col2:
    st.image("https://cdn.pixabay.com/photo/2017/11/26/15/16/smiley-2979107_1280.jpg", width=100)

# Create button to save mood
if st.button("📌 Log Mood"):
    save_mood_data(today, mood)
    st.success("✅ Mood Logged Successfully!")

# Load existing mood data
data = load_mood_data()

# If there is data to display
if not data.empty:
    st.subheader("📊 Mood Trends Over Time")

    # Convert date strings to datetime objects
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    # Remove any rows with NaN values in Date or Mood
    data = data.dropna(subset=["Date", "Mood"])

    # Count occurrences of each mood
    mood_counts = data["Mood"].value_counts()

    # ✅ Fix: Ensure the chart is only created if there is valid data
    if not mood_counts.empty:
        st.bar_chart(mood_counts)
    else:
        st.warning("⚠️ No mood data available yet. Start logging your moods!")

# Footer with credit
st.markdown("---")
st.markdown("Designed with  by [Aamna Ansari ❤️]")
