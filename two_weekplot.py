import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("Plot the Last 21 Daily Data Points")
# 添加中文字体支持（示例使用微软雅黑，请确保系统有该字体）
# 也可以替换为其他中文字体路径如 "simhei.ttf"
chinese_font = ImageFont.truetype("SimHei.ttf", 12)  # 调整字体大小

fm.fontManager.addfont('SimHei.ttf')
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
        ax.set_title("耳鸣级数 (past 21 days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.set_xticks(dates)
        ax.set_xticklabels([d.strftime("%m-%d") for d in dates], rotation=45)
        st.pyplot(fig)

    except ValueError:
        st.error("Please ensure all inputs are valid numbers.")
