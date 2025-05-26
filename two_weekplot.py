import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("Plot the Last 21 Daily Data Points")

# Text input area
data_input = st.text_area("Paste your series of numbers (comma or newline separated):", height=200)

if data_input:
    # Split and clean input
    raw_data = [x.strip() for x in data_input.replace(',', '\n').split('\n')]
    
    try:
        # Convert to float and take last 21
        numbers = [float(x) for x in raw_data if x]
        last_21 = numbers[-21:]
        num_points = len(last_21)

        # Generate dates ending today
        today = datetime.today().date()
        dates = [today - timedelta(days=i) for i in range(num_points-1, -1, -1)]

        st.write(f"Plotting data for the last {num_points} day(s), ending {today}:")
        
        # Plotting
        fig, ax = plt.subplots()
        ax.plot(dates, last_21, marker='o')
        ax.set_title("Daily Data (Last 21 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    except ValueError:
        st.error("Please ensure all inputs are valid numbers.")
