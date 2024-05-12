import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np

# Define the two points and angle
point1 = (0, 0)
point2 = (4, 4)
angle_degrees = 45

# Plot the two lines
plt.plot([0, point1[0]], [0, point1[1]], label='Line 1')
plt.plot([0, point2[0]], [0, point2[1]], label='Line 2')

# Calculate the radius of the arc
radius = 1  # Adjust this value to change the radius of the arc

# Calculate the angle in radians
angle_radians = np.deg2rad(angle_degrees)

# Create the arc
arc = Arc((0, 0), radius * 2, radius * 2, angle=0, theta1=0, theta2=angle_degrees)

# Add the arc to the plot
plt.gca().add_patch(arc)

# Set equal aspect ratio for better visualization
plt.gca().set_aspect('equal', adjustable='box')

# Set limits for better visualization
plt.xlim(-1, max(point1[0], point2[0]) + 1)
plt.ylim(-1, max(point1[1], point2[1]) + 1)

# Add legend
plt.legend()

# Show plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Arc between Two Points')
plt.grid(True)
plt.show()
