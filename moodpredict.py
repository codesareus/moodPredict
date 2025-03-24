import streamlit as st
import matplotlib.pyplot as plt
import time

# Set Streamlit page config to dark mode
st.set_page_config(layout="wide", page_title="Crane Flight Animation", page_icon="🕊️")

st.title("Crane Flight Animation")

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('black')  # Dark background

# Environment setup
def draw_environment():
    # Ground
    ax.fill_between([0, 1000], 0, 50, color='darkgreen', alpha=0.6)  # Darker ground
    # Clouds
    ax.scatter([200, 600, 800], [400, 350, 450], s=150, c='lightgray', alpha=0.7)  # Lighter clouds
    # Sun
    ax.scatter(900, 450, s=900, c='yellow', alpha=0.8)  # Bright sun
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.axis('off')

draw_environment()

# Initialize crane
crane, = ax.plot([], [], marker='o', markersize=20, 
                markerfacecolor='lightgray', markeredgecolor='white', linestyle='none')  # Lighter crane

# Animation parameters
max_frames = 150
frame_delay = 0.05  # seconds

# Create a placeholder for the plot
plot_placeholder = st.empty()

# Animation loop
for frame in range(max_frames):
    # Calculate position
    if frame < 50:
        x = [50 + frame * 8]
        y = [400]
    elif 50 <= frame < 100:
        t = frame - 50
        x = [450 + t * 8]
        y = [400 - 0.14 * t**2]
    else:
        x = [850]
        y = [50]
    
    # Update crane position
    crane.set_data(x, y)
    
    # Redraw plot
    plot_placeholder.pyplot(fig)
    time.sleep(frame_delay)
    
    # Clear for next frame (prevent ghosting)
    crane.set_data([], [])

# Reset plot after animation
draw_environment()
plot_placeholder.pyplot(fig)
