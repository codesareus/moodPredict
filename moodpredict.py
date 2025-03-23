import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from IPython.display import HTML

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

# Convert the animation to HTML
html = ani.to_jshtml()

# Embed the HTML in Streamlit
st.components.v1.html(html, height=600)

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

# Use Streamlit's `st.pyplot` to display the initial plot
st.pyplot(fig)

# Use HTML to embed the animation
st.write("If the animation doesn't play automatically, refresh the page or use the controls below.")
st.components.v1.html(ani.to_jshtml(), height=600)
