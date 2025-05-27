import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.font_manager as fm

# Add the SimHei font to Matplotlib's font manager
fm.fontManager.addfont('SimHei.ttf')  # Ensure 'SimHei.ttf' is in your working directory

st.title("Plot the Last 21 Daily Data Points with Moving Average")
data_input = st.text_area("Paste your series of numbers (comma or newline separated):", height=200)

if data_input:
    raw_data = [x.strip() for x in data_input.replace(',', '\n').split('\n')]
    
    try:
        numbers = [float(x) for x in raw_data if x]
        if len(numbers) < 27:
            st.error("Need at least 27 data points for accurate moving average calculation")
        else:
            # Get last 27 days to calculate 21-point moving average
            last_27 = numbers[-27:]
            
            # Generate dates for last 21 days
            today = datetime.today().date()
            dates = [today - timedelta(days=i) for i in range(20, -1, -1)]  # Last 21 days
            
            # Calculate 7-day moving average (21 points from 27-day window)
            moving_avg = [sum(last_27[i:i+7])/7 for i in range(21)]
            
            # Get last 21 days of original data
            original_data = last_27[-21:]

            st.write(f"Plotting data for the last 21 days ending {today}:")
            
            # Configure plot
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            fig, ax = plt.subplots()
            ax.plot(dates, original_data, marker='o', label='Daily Data')
            ax.plot(dates, moving_avg, label='7-Day Moving Average', 
                    color='orange', linestyle='--', linewidth=2)
            
            ax.set_title("耳鸣级数 (21-Day Trend with Moving Average)")
            ax.set_xlabel("Date")
            ax.set_ylabel("Value")
            ax.set_xticks(dates)
            ax.set_xticklabels([d.strftime("%m-%d") for d in dates], rotation=45)
            ax.legend()
            st.pyplot(fig)

    except ValueError:
        st.error("Please ensure all inputs are valid numbers.")
