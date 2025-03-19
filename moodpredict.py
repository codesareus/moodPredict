
import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pytz

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

def init_session_state():
    if "mood_history" not in st.session_state:
        st.session_state.mood_history = pd.DataFrame(columns=[
            "Date", "Sentence 1", "Sentence 2", 
            "Predicted Mood", "Mood Score", "Emoji"
        ])

st.set_page_config(page_title="Mood Diary", page_icon="📔")
st.title("📔 Daily Mood Diary")
st.write("Document your daily mood with two sentences!")

# Allow user to upload a CSV file
uploaded_file = st.file_uploader("Upload your mood history CSV", type=["csv"])
if uploaded_file is not None:
    st.session_state.mood_history = pd.read_csv(uploaded_file, parse_dates=["Date"])

init_session_state()

st.write("## Daily Entry")

# Determine if today's entry exists
today_date = datetime.now().date()
submitted_today = False
if not st.session_state.mood_history.empty and 'Date' in st.session_state.mood_history:
    submitted_today = today_date in pd.to_datetime(st.session_state.mood_history["Date"]).dt.date.values

with st.form("daily_entry"):
    sentence1 = st.text_area("First sentence:", disabled=submitted_today,
                             placeholder="How are you feeling today?", height=68)
    sentence2 = st.text_area("Second sentence:", disabled=submitted_today,
                             placeholder="What's been on your mind?", height=68)
    submitted = st.form_submit_button("Save Today's Entry", disabled=submitted_today)

def analyze_mood(sentence1, sentence2):
    combined_text = f"{sentence1} {sentence2}"
    analysis = TextBlob(combined_text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.3:
        mood = "Happy"
    elif polarity < -0.3:
        mood = "Sad"
    else:
        mood = "Neutral"
        
    return mood, polarity, MOOD_EMOJIS.get(mood, "")

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
    
    new_entry_df = pd.DataFrame([new_entry])
    st.session_state.mood_history = pd.concat([st.session_state.mood_history, new_entry_df], ignore_index=True)
    
    # Save to server CSV only if no file was uploaded
    if uploaded_file is None:
        new_entry_df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
    
    st.success("Entry saved successfully!")
    st.balloons()
    submitted_today = True  # Immediately reflect the submission

elif submitted:
    st.warning("Please fill in both sentences!")

if submitted_today:
    st.subheader("Today's Mood")
    col1, col2, col3 = st.columns(3)
    today_entry = st.session_state.mood_history.iloc[-1]
    with col1:
        st.metric("Predicted Mood", f"{today_entry['Predicted Mood']} {today_entry['Emoji']}")
    with col2:
        st.metric("Mood Score", f"{today_entry['Mood Score']:.2f}")
    with col3:
        csv = st.session_state.mood_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download History",
            data=csv,
            file_name="mood_history.csv",
            mime="text/csv"
        )

if not st.session_state.mood_history.empty:
    st.subheader("Your Mood History")
    display_df = st.session_state.mood_history.tail(5).copy()
    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.strftime("%Y-%m-%d")
    st.dataframe(display_df.style.format({"Mood Score": "{:.2f}"}))

    st.subheader("Mood Timeline (Current Month)")
    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_data = st.session_state.mood_history[
        (pd.to_datetime(st.session_state.mood_history["Date"]).dt.month == current_month) &
        (pd.to_datetime(st.session_state.mood_history["Date"]).dt.year == current_year)
    
    if not monthly_data.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(pd.to_datetime(monthly_data["Date"]), monthly_data["Mood Score"], 
                marker='o', linestyle='-', color='skyblue', label="Mood Score")
        
        for date, score, emoji in zip(pd.to_datetime(monthly_data["Date"]), monthly_data["Mood Score"], monthly_data["Emoji"]):
            ax.text(date, score + 0.02, emoji, fontsize=12, ha='center', va='bottom', color="orange")
        
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d'))
        plt.xticks(rotation=45)
        ax.set_xlabel("Day of Month")
        ax.set_ylabel("Mood Score")
        ax.set_title(f"Mood Timeline ({datetime.now().strftime('%B %Y')})")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("No data available for the current month.")

st.markdown("---")
st.caption("Your personal mood diary - Reflect, remember, and grow.")
