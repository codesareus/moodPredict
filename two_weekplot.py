import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz  # Needed for timezone handling
import matplotlib.font_manager as fm

# Add the SimHei font to Matplotlib's font manager
fm.fontManager.addfont('SimHei.ttf')

st.title("Plot the Last 21 Daily Data Points with Moving Average (Central Time)")

# Configure Central Time zone
cst = pytz.timezone('America/Chicago')

def get_cst_date():
    """Get current date in US Central Time"""
    now_utc = datetime.now(pytz.utc)
    return now_utc.astimezone(cst).date()

data_input = st.text_area("Paste your series of numbers (comma or newline separated):", height=200)

if data_input:
    raw_data = [x.strip() for x in data_input.replace(',', '\n').split('\n')]
    
    try:
        numbers = [float(x) for x in raw_data if x]
        if len(numbers) < 27:
            st.error("Need at least 27 data points for accurate moving average calculation")
        else:
            # Get current date in Central Time
            today_cst = get_cst_date()
            
            # Generate dates for last 21 days (CST)
            dates = [today_cst - timedelta(days=i) for i in range(20, -1, -1)]  # Last 21 days
            
            # Get relevant data (last 27 days to calculate 21-day moving average)
            last_27 = numbers[-27:]
            
            # Calculate 7-day moving average
            moving_avg = [sum(last_27[i:i+7])/7 for i in range(21)]
            
            # Get last 21 days of original data
            original_data = last_27[-21:]

            st.write(f"Plotting data for Central Time dates {dates[0]} to {dates[-1]}:")
            
            # Configure plot
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates, original_data, marker='o', label='Daily Data')
            ax.plot(dates, moving_avg, label='7-Day Moving Average', 
                    color='orange', linestyle='--', linewidth=2)
            
            ax.set_title("Tinnitus Severity Level (21-Day Trend with Moving Average)")
            ax.set_xlabel("Date (Central Time)")
            ax.set_ylabel("Value")
            ax.set_xticks(dates)
            ax.set_xticklabels([d.strftime("%m-%d\n%a") for d in dates], rotation=0)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format dates in both Western and Chinese style
            ax.set_xlabel(f"Date (Central Time)\n{today_cst.strftime('%Y-%m-%d')}")
            st.pyplot(fig)

    except ValueError:
        st.error("Please ensure all inputs are valid numbers.")
    except pytz.UnknownTimeZoneError:
        st.error("Timezone configuration error - please ensure pytz is installed.")
