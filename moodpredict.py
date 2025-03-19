
import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pytz  # Requires `pytz` library

# Configuration
CSV_FILE = "mood_history.csv"
MOOD_EMOJIS = {
    'Happy': '😊', 
    'Sad': '😢',
    'Energetic': '💪',
    'Calm': '🧘',
    'Creative': '🎨',
    'Stressed': '😰',
    'Neutral': '😐'
}

# Initialize session state and load existing data
def init_session_state():
    if "mood_history" not in st.session_state:
        # Check if a local file is uploaded
        uploaded_file = st.session_state.get("uploaded_file")
        if uploaded_file:
            # Load the uploaded file into session state
            st.session_state.mood_history = pd.read_csv(uploaded_file)
        elif os.path.exists(CSV_FILE):
            # Fallback to server-side CSV if no file is uploaded
            st.session_state.mood_history = pd.read_csv(CSV_FILE, parse_dates=["Date"])
        else:
            # Initialize an empty DataFrame if no file exists
            st.session_state.mood_history = pd.DataFrame(columns=[
                "Date", "Sentence 1", "Sentence 2", 
                "Predicted Mood", "Mood Score", "Emoji"
            ])
            
    if "submitted_today" not in st.session_state:
        today = datetime.now().date()
        st.session_state.submitted_today = today in st.session_state.mood_history["Date"].dt.date.values

# Configure page
st.set_page_config(page_title="Mood Diary", page_icon="📔")
st.title("📔 Daily Mood Diary")
st.write("Document your daily mood with two sentences!")

def analyze_mood(sentence1, sentence2):
    combined_text = f"{sentence1} {sentence2}"
    analysis = TextBlob(combined_text)
    polarity = analysis.sentiment.polarity
    
    # Simplified mood detection for example
    if polarity > 0.3:
        mood = "Happy"
    elif polarity < -0.3:
        mood = "Sad"
    else:
        mood = "Neutral"
        
    return mood, polarity, MOOD_EMOJIS.get(mood, "")

def save_to_csv():
    st.session_state.mood_history.to_csv(CSV_FILE, index=False)

# Initialize the app
init_session_state()

# Allow users to upload a local file
uploaded_file = st.file_uploader("Upload a local CSV file", type=["csv"])
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    init_session_state()  # Reload session state with the uploaded file

# Main input form
with st.form("daily_entry"):
    st.subheader("Today's Entry")
    
    sentence1 = st.text_area("First sentence:", 
                           disabled=st.session_state.submitted_today,
                           placeholder="How are you feeling today?", height=68)
    
    sentence2 = st.text_area("Second sentence:", 
                           disabled=st.session_state.submitted_today,
                           placeholder="What's been on your mind?", height=68)
    
    submitted = st.form_submit_button("Save Today's Entry", 
                                    disabled=st.session_state.submitted_today)

# Handle form submission
if submitted and sentence1.strip() and sentence2.strip():
    mood, score, emoji = analyze_mood(sentence1, sentence2)
    today = datetime.now()
    
    new_entry = {
        "Date": today,
        "Sentence 1": sentence1,
        "Sentence 2": sentence2,
        "Predicted Mood": mood,
        "Mood Score": round(score, 2),
        "Emoji": emoji
    }
    
    # Append the new entry to the server-side CSV file
    new_entry_df = pd.DataFrame([new_entry])
    new_entry_df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
    
    # Reload the mood history from the CSV file
    st.session_state.mood_history = pd.read_csv(CSV_FILE, parse_dates=["Date"])
    
    st.session_state.submitted_today = True
    st.success("Entry saved successfully!")
    st.balloons()

elif submitted:
    st.warning("Please fill in both sentences!")

# Display today's mood if available
if st.session_state.submitted_today:
    today = datetime.now().date()
    today_entry = st.session_state.mood_history[
        st.session_state.mood_history["Date"].dt.date == today
    ].iloc[-1]  # Get the latest entry for today
    
    st.subheader("Today's Mood")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Predicted Mood", f"{today_entry['Predicted Mood']} {today_entry['Emoji']}")
    with col2:
        st.metric("Mood Score", f"{today_entry['Mood Score']:.2f}")
    with col3:
        st.write("")
        if not st.session_state.mood_history.empty:
            with open("mood_history.csv", "rb") as file:
                st.download_button(
                    label="点击下载History文件",
                    data=file,
                    file_name="Mood_history.csv",
                    mime="text/csv"
                )
        else:
            st.error("没有可下载的数据，请先输入数据并保存。")

# Display mood history
if not st.session_state.mood_history.empty:
    st.subheader("Your Mood History")
    
    # Display dataframe with formatted dates
    display_df = st.session_state.mood_history.copy().tail(5)
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df.style.format({"Mood Score": "{:.2f}"}))
    
    # Plotting section (current month only)
    st.subheader("Mood Timeline (Current Month)")
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter data for the current month
    st.session_state.mood_history["Date"] = pd.to_datetime(st.session_state.mood_history["Date"]).dt.tz_localize(None)
    monthly_data = st.session_state.mood_history[
        (st.session_state.mood_history["Date"].dt.month == current_month) &
        (st.session_state.mood_history["Date"].dt.year == current_year)
    ]

    if not monthly_data.empty:
        # Create a complete date range for the current month
        first_day = datetime(current_year, current_month, 1)
        last_day = datetime(current_year, current_month + 1, 1) - pd.Timedelta(days=1)
        date_range = pd.date_range(first_day, last_day, freq="D")

        # Create a DataFrame with the full date range
        full_month_df = pd.DataFrame(date_range, columns=["Date"])
        full_month_df = full_month_df.merge(monthly_data, on="Date", how="left")

        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(full_month_df["Date"], full_month_df["Mood Score"], 
                marker='o', linestyle='-', color='skyblue', label="Mood Score")
        
        # Add emojis for days with data
        for date, score, emoji in zip(full_month_df["Date"], full_month_df["Mood Score"], full_month_df["Emoji"]):
            if not pd.isna(score):  # Only plot emojis for days with data
                ax.text(date, score + 0.0002, emoji, 
                        fontsize=24, ha='center', va='bottom', color="orange")
        
        # Set x-axis limits to the first and last day of the month
        ax.set_xlim(first_day, last_day)
        
        # Format x-axis to show only the day of the month
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d'))  # Show only day
        plt.xticks(rotation=45)
        ax.set_xlabel("Day of Month")
        ax.set_ylabel("Mood Score")
        ax.set_title(f"Your Mood Over Time ({first_day.strftime('%B %Y')})")  # Show month and year in title
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("No data available for the current month.")
        
    # Download button
    csv = st.session_state.mood_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full History",
        data=csv,
        file_name="mood_diary.csv",
        mime="text/csv"
    )

# Display message if already submitted today
if st.session_state.submitted_today:
    st.info("You've already made an entry for today. Come back tomorrow!")

# Footer
st.markdown("---")
st.caption("Your personal mood diary - Reflect, remember, and grow.")
