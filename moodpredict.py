
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.title("Crane Flight Animation")
st.write("Watch the crane fly across the sky and land gracefully!")

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('lightblue')

# Environment setup
def draw_environment():
    # Ground
    ax.fill_between([0, 1000], 0, 50, color='olive', alpha=0.6)
    # Clouds
    ax.scatter([200, 600, 800], [400, 350, 450], s=150, c='white', alpha=0.7)
    # Sun
    ax.scatter(900, 450, s=300, c='gold', alpha=0.8)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.axis('off')

draw_environment()

# Initialize crane (now using a proper line object)
crane, = ax.plot([], [], marker='o', markersize=20, 
                markerfacecolor='gray', markeredgecolor='black', linestyle='-')

def init():
    crane.set_data([], [])
    return crane,

def update(frame):
    if frame < 50:
        x = [50 + frame * 8]  # Wrap in list
        y = [400]
    elif 50 <= frame < 100:
        t = frame - 50
        x = [450 + t * 8]
        y = [400 - 0.14 * t**2]
    else:
        x = [850]
        y = [50]
        
    crane.set_data(x, y)
    return crane,

ani = animation.FuncAnimation(fig, update, frames=150,
                              init_func=init, blit=True, interval=50, repeat=True)

# Convert animation to HTML
with st.container():
    st.components.v1.html(ani.to_jshtml(), height=600)
