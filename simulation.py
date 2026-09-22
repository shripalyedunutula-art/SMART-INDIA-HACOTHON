import matplotlib.pyplot as plt
import numpy as np
import time

# 1. Setup the road boundaries (Unstructured road, no lane markings)
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))

# Car starting position and destination
car_x, car_y = 0, 2.5
dest_x, dest_y = 10, 2.5

# Unpredictable obstacles (e.g., Pothole, Stray Animal)
obstacles = np.array([[4.0, 2.7], [7.0, 2.0]]) 
sensor_radius = 2.5 # Simulated Onboard/Satellite Detection Zone

# Path planning loop
for step in range(50):
    ax.clear()
    
    # Draw road limits
    ax.axhline(y=0, color='black', linestyle='--', label='Road Edge')
    ax.axhline(y=5, color='black', linestyle='--')
    
    # Plot destination and obstacles
    ax.scatter(dest_x, dest_y, color='gold', s=200, marker='*', label='Destination')
    ax.scatter(obstacles[:,0], obstacles[:,1], color='red', s=300, marker='X', label='Obstacles (Potholes/Cattle)')
    
    # Sensor detection zone
    sensor_zone = plt.Circle((car_x, car_y), sensor_radius, color='cyan', fill=True, alpha=0.15, label='Sensor Radius')
    ax.add_patch(sensor_zone)
    
    # Core Logic: Adaptive Path Correction
    avoiding = False
    for obs in obstacles:
        # Check if obstacle is within sensor range and in the way
        distance = np.linalg.norm(np.array([car_x, car_y]) - obs)
        if distance < sensor_radius and abs(car_x - obs[0]) < 1.5:
            # Dodge maneuver: Change Y coordinates to avoid obstacle
            car_y = obs[1] - 1.2 if obs[1] > 2.5 else obs[1] + 1.2
            avoiding = True
            break
            
    if not avoiding:
        # Move smoothly back towards the center path
        car_y = car_y + 0.1 * (2.5 - car_y)

    # Move vehicle forward
    car_x += 0.2
    
    # Plot Car
    ax.scatter(car_x, car_y, color='blue', s=150, marker='o', label='Our Autonomous Car')
    
    # Formatting the plot
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 6)
    ax.set_title("SIH 2026: Adaptive Path Planning & Sensor Fusion Prototype")
    ax.legend(loc='upper left')
    
    plt.draw()
    plt.pause(0.1)
    
    if car_x >= dest_x:
        print("Destination reached safely!")
        break

plt.ioff()
plt.show()

