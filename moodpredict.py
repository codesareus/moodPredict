import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Set up the figure and axis
fig, ax = plt.subplots()

# Initial crane position (x, y)
crane_x = np.linspace(0, 10, 100)  # Horizontal movement
crane_y = np.linspace(10, 0, 100)  # Vertical movement (descending)

# Ground line
ground_x = np.linspace(-2, 12, 100)
ground_y = np.zeros_like(ground_x)

# Initialize the crane plot
crane, = ax.plot([], [], 'bo', markersize=20)  # Crane as a blue dot
ground, = ax.plot(ground_x, ground_y, 'g-', linewidth=2)  # Green ground line

# Set axis limits
ax.set_xlim(-2, 12)
ax.set_ylim(-1, 12)

# Labels
ax.set_xlabel("Distance")
ax.set_ylabel("Height")
ax.set_title("Crane Flying and Landing")

# Animation function
def animate(i):
    crane.set_data(crane_x[i], crane_y[i])  # Update crane position
    return crane,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(crane_x), interval=50, blit=True)

# Display the animation in Streamlit
st.title("Crane Flying and Landing Animation")
st.write("Watch the crane fly through the sky, descend, and land on the ground!")
st.pyplot(fig)

# To display the animation, we need to use st.write with HTML
st.write("If the animation doesn't play automatically, refresh the page or use the controls below.")
st.write(ani.to_jshtml(), unsafe_allow_html=True)
