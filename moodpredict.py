import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties

# Configure page
st.set_page_config(page_title="Mood Predictor", page_icon="😊")
st.title("🌈 Daily Mood Predictor")
st.write("Describe your day in two sentences, and I'll predict your mood!")

# Initialize session state for mood history
if "mood_history" not in st.session_state:
    st.session_state.mood_history = pd.DataFrame(columns=["Date", "Sentence 1", "Sentence 2", "Predicted Mood", "Mood Score"])

# Mood database with sentence-level keywords
MOOD_KEYWORDS = {
    'happy': ['joy', 'excited', 'celebrate', 'love', 'fun', 'smile', 'amazing'],
    'sad': ['sad', 'lonely', 'cry', 'hurt', 'miss', 'loss', 'depressed'],
    'energetic': ['energy', 'active', 'workout', 'run', 'dance', 'motivated'],
    'calm': ['peaceful', 'relax', 'calm', 'serene', 'meditate', 'yoga'],
    'creative': ['create', 'art', 'write', 'design', 'paint', 'music'],
    'stressed': ['stress', 'busy', 'overwhelmed', 'deadline', 'pressure']
}

# Sentiment thresholds
MOOD_THRESHOLDS = {
    '😢 Sad': (-1.0, -0.3),
    '😐 Neutral': (-0.3, 0.3),
    '😊 Happy': (0.3, 1.0)
}

# Emoji mapping
MOOD_EMOJIS = {
    'Happy': '😊', 
    'Sad': '😢',
    'Energetic': '💪',
    'Calm': '🧘',
    'Creative': '🎨',
    'Stressed': '😰',
    'Neutral': '😐'
}

def analyze_mood(sentence1, sentence2):
    # Combine sentences for sentiment analysis
    combined_text = f"{sentence1} {sentence2}"
    
    # Sentiment analysis
    analysis = TextBlob(combined_text)
    polarity = analysis.sentiment.polarity
    
    # Keyword matching for mood
    matched_moods = []
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined_text.lower():
                matched_moods.append(mood)
    
    # Combine results
    if len(matched_moods) > 0:
        primary_mood = max(set(matched_moods), key=matched_moods.count)
    else:
        for mood, (low, high) in MOOD_THRESHOLDS.items():
            if low <= polarity <= high:
                primary_mood = mood
                break
    
    return primary_mood.capitalize() if isinstance(primary_mood, str) else primary_mood, polarity

# User inputs
st.subheader("Describe your day:")
sentence1 = st.text_area("First sentence:", placeholder="e.g., I woke up feeling refreshed and ready for the day.")
sentence2 = st.text_area("Second sentence:", placeholder="e.g., I had a great time with my friends at lunch.")

if st.button("Predict My Mood!"):
    if sentence1.strip() and sentence2.strip():
        mood, score = analyze_mood(sentence1.lower(), sentence2.lower())
        
        # Add to mood history
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Sentence 1": sentence1,
            "Sentence 2": sentence2,
            "Predicted Mood": mood,
            "Mood Score": score
        }
        st.session_state.mood_history = pd.concat([st.session_state.mood_history, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Display result
        st.subheader(f"Predicted Mood: {MOOD_EMOJIS.get(mood, '')} {mood}")
        st.write(f"Mood Score: {score:.2f}")
        st.balloons()
    else:
        st.warning("Please enter both sentences!")

# Display mood history
if not st.session_state.mood_history.empty:
    st.subheader("Your Mood History")
    st.dataframe(st.session_state.mood_history)

    # Plot mood scores over time
    st.subheader("Daily Mood Score Trend")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the mood scores
    dates = pd.to_datetime(st.session_state.mood_history["Date"])
    scores = st.session_state.mood_history["Mood Score"]
    ax.plot(dates, scores, marker='o', linestyle='-', color='skyblue', label="Mood Score")
    
    # Add emojis on top of data points
    try:
        # Use a font that supports emojis (adjust the path as needed for your system)
        emoji_font_path = "NotoColorEmoji-Regular.ttf"  # e.g., "Segoe UI Emoji" on Windows
        emoji_font = FontProperties(fname=emoji_font_path)
        
        for i, (date, score, mood) in enumerate(zip(dates, scores, st.session_state.mood_history["Predicted Mood"])):
            # Fetch the emoji for the current mood
            emoji = MOOD_EMOJIS.get(mood.capitalize(), '')  # Ensure mood is capitalized
            ax.text(date, score + 0.05, emoji, 
                    fontsize=24, ha='center', va='bottom', fontproperties=emoji_font)  # Use emoji-compatible font
            
        # Debugging: Verify emojis are fetched correctly
        st.write(f"Debug: Emoji for '{mood}' is {emoji}")
    except Exception as e:
        st.error(f"Error rendering emojis: {e}. Please ensure the font supports emojis.")
    
    # Format the x-axis dates
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)  # Rotate dates for better readability
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Mood Score")
    ax.set_title("Your Mood Over Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Download mood history as CSV
    csv = st.session_state.mood_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Mood History as CSV",
        data=csv,
        file_name="mood_history.csv",
        mime="text/csv"
    )

# Add a fun footer
st.markdown("---")
st.caption("Made with ❤️ by Your Mood Predictor. Reflect on your day and embrace your feelings!")
