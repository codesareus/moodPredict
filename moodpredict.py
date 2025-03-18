import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pytz

# Configure timezone (Chicago)
tz = pytz.timezone("America/Chicago")
today = datetime.now(tz)  # Timezone-aware datetime object

CSV_FILE = "mood_history.csv"
MOOD_EMOJIS = {
    'Happy': '😊', 'Sad': '😢', 'Energetic': '💪',
    'Calm': '🧘', 'Creative': '🎨', 'Stressed': '😰', 'Neutral': '😐'
}

def init_session_state():
    if "mood_history" not in st.session_state:
        if os.path.exists(CSV_FILE):
            # Read and localize dates to Chicago timezone
            df = pd.read_csv(CSV_FILE, parse_dates=["Date"])
            df["Date"] = df["Date"].dt.tz_localize(tz)
            st.session_state.mood_history = df
        else:
            st.session_state.mood_history = pd.DataFrame(columns=[
                "Date", "Sentence 1", "Sentence 2", 
                "Predicted Mood", "Mood Score", "Emoji"
            ])
    
    # Check submissions using timezone-aware date
    today_date = today.date()
    exists = False
    if not st.session_state.mood_history.empty:
        exists = today_date in st.session_state.mood_history["Date"].dt.date.values
    st.session_state.submitted_today = exists

# Page configuration
st.set_page_config(page_title="Mood Diary", page_icon="📔")
st.title("📔 Daily Mood Diary")
st.write("Document your daily mood with two sentences!")

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

def save_to_csv():
    st.session_state.mood_history.to_csv(CSV_FILE, index=False)

# Initialize app
init_session_state()

# Main input form
with st.form("daily_entry"):
    st.subheader("Today's Entry")
    sentence1 = st.text_area("First sentence:", disabled=st.session_state.submitted_today,
                           placeholder="How are you feeling today?", height=68)
    sentence2 = st.text_area("Second sentence:", disabled=st.session_state.submitted_today,
                           placeholder="What's been on your mind?", height=68)
    submitted = st.form_submit_button("Save Today's Entry", 
                                    disabled=st.session_state.submitted_today)

# Handle submission
if submitted and sentence1.strip() and sentence2.strip():
    mood, score, emoji = analyze_mood(sentence1, sentence2)
    
    new_entry = {
        "Date": today.astimezone(tz).replace(tzinfo=None),  # Store as naive datetime in Chicago time
        "Sentence 1": sentence1,
        "Sentence 2": sentence2,
        "Predicted Mood": mood,
        "Mood Score": round(score, 2),
        "Emoji": emoji
    }
    
    # Update data
    new_entry_df = pd.DataFrame([new_entry])
    header = not os.path.exists(CSV_FILE)
    new_entry_df.to_csv(CSV_FILE, mode='a', header=header, index=False)
    
    # Reload data with proper timezone
    df = pd.read_csv(CSV_FILE, parse_dates=["Date"])
    df["Date"] = df["Date"].dt.tz_localize(tz)
    st.session_state.mood_history = df
    
    st.session_state.submitted_today = True
    st.success("Entry saved successfully!")
    st.balloons()

elif submitted:
    st.warning("Please fill in both sentences!")

# Display today's mood
if st.session_state.submitted_today:
    today_date = today.date()
    today_entry = st.session_state.mood_history[
        st.session_state.mood_history["Date"].dt.date == today_date
    ].iloc[-1]
    
    st.subheader("Today's Mood")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Predicted Mood", f"{today_entry['Predicted Mood']} {today_entry['Emoji']}")
    with col2:
        st.metric("Mood Score", f"{today_entry['Mood Score']:.2f}")

# Mood history and visualization
if not st.session_state.mood_history.empty:
    st.subheader("Your Mood History")
    display_df = st.session_state.mood_history.copy().tail(5)
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df.style.format({"Mood Score": "{:.2f}"}))
    
    # Visualization
    st.subheader("Mood Timeline (Current Month)")
    current_month = today.month
    current_year = today.year
    
    monthly_data = st.session_state.mood_history[
        (st.session_state.mood_history["Date"].dt.month == current_month) &
        (st.session_state.mood_history["Date"].dt.year == current_year)
    ]
    
    if not monthly_data.empty:
        # Create complete date range for Chicago timezone
        first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = (first_day + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
        date_range = pd.date_range(first_day, last_day, freq="D", tz=tz)
        
        full_month_df = pd.DataFrame({"Date": date_range})
        full_month_df = full_month_df.merge(monthly_data, on="Date", how="left")
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(full_month_df["Date"], full_month_df["Mood Score"], 
                marker='o', linestyle='-', color='skyblue')
        
        for date, score, emoji in zip(full_month_df["Date"], full_month_df["Mood Score"], full_month_df["Emoji"]):
            if not pd.isna(score):
                ax.text(date, score + 0.02, emoji, fontsize=12, ha='center', va='bottom')
        
        ax.set_xlim(first_day, last_day)
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d\n%a', tz=tz))
        plt.xticks(rotation=45)
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood Score")
        ax.set_title(f"Mood Timeline - {first_day.strftime('%B %Y')}")
        st.pyplot(fig)
    else:
        st.info("No data available for the current month.")

# Footer
st.markdown("---")
st.caption("Your personal mood diary - Reflect, remember, and grow.")
