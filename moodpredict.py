import streamlit as st
import matplotlib.pyplot as plt
import time

# Streamlit setup
st.title("Crane Flight Animation")
st.write("Watch the crane fly across the sky and land gracefully!")

# Initialize session state for animation control
if 'frame' not in st.session_state:
    st.session_state.frame = 0

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('lightblue')  # Sky background

# Animation parameters
max_frames = 150
ground_level = 50  # Y-coordinate for ground

def draw_environment():
    """Draw sky and ground"""
    # Ground
    ax.add_patch(plt.Rectangle((0, 0), 1000, ground_level, 
                              color='olive', alpha=0.6))
    # Clouds
    ax.scatter([200, 600, 800], [400, 350, 450], s=150, c='white', alpha=0.7)
    
    # Sun
    ax.scatter(900, 450, s=300, c='gold', alpha=0.8)

def calculate_position(frame):
    """Calculate crane position based on frame number"""
    if frame < 50:
        # Flying phase: move right across the sky
        x = 50 + frame * 8
        y = 400
    elif 50 <= frame < 100:
        # Descending phase: parabolic descent
        t = frame - 50
        x = 450 + t * 8
        y = 400 - 0.14 * t**2
    else:
        # Landing phase: stay on ground
        x = 850
        y = ground_level
        
    return x, y

# Main animation loop
with st.container():
    # Create a placeholder for the plot
    plot_placeholder = st.empty()
    
    # Draw initial environment
    draw_environment()
    
    # Draw crane
    x, y = calculate_position(st.session_state.frame)
    crane = ax.plot(x, y, marker='o', markersize=20, 
                   markerfacecolor='gray', markeredgecolor='black')[0]
    
    # Add some style
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.axis('off')  # Hide axes
    
    # Update plot in placeholder
    plot_placeholder.pyplot(fig)
    
    # Control animation
    if st.session_state.frame < max_frames:
        st.session_state.frame += 1
        time.sleep(0.05)
        st.rerun()
    else:
        st.session_state.frame = 0  # Reset when animation completes
