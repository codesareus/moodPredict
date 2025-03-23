
import streamlit as st
import matplotlib.pyplot as plt
import time

st.title("Crane Night Flight Animation")

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('#1A1F2C')  # Dark navy blue background

# Environment setup
def draw_environment():
    # Ground (darker green)
    ax.fill_between([0, 1000], 0, 50, color='#2D423F', alpha=0.9)
    
    # Moon (large and bright)
    ax.scatter(850, 450, s=2000,  # Larger size
               c='#FFFCDC',       # Soft yellow-white
               alpha=0.95,
               edgecolor='white',
               linewidth=1.5)
    
    # Stars (new addition)
    ax.scatter(
        [100, 250, 400, 600, 750, 900],
        [420, 380, 450, 350, 410, 470],
        s=15, c='white', alpha=0.7
    )
    
    # Clouds (lighter for contrast)
    ax.scatter([150, 500, 750], [400, 350, 420], 
               s=200,             # Larger clouds
               c='#C7C9C7',       # Light gray
               alpha=0.3,
               edgecolor='white') # Subtle outline
    
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.axis('off')

draw_environment()

# Initialize crane (brighter color for visibility)
crane, = ax.plot([], [], marker='o', markersize=25, 
                markerfacecolor='#FFFCDC',  # Match moon color
                markeredgecolor='white',
                linestyle='none',
                alpha=0.9)

# Animation parameters
max_frames = 150
frame_delay = 0.06  # Slightly slower for better visibility

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
    
    # Clear for next frame
    crane.set_data([], [])

# Reset plot after animation
draw_environment()
plot_placeholder.pyplot(fig)
