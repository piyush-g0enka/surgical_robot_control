import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
m = 10  # mass in kg
b = 70  # damping coefficient in N*s/m
k = 1000  # spring constant (N/m)
delta_t = 0.001  # time step in seconds

# Read the data from the CSV file
file_path = 'data.csv'  # Update with the actual path to your CSV file
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
print(data.head())

# Assuming the CSV contains 'time' and 'force' columns
time = data['time'].values  # time data from the CSV file
force_data = data['force'].values  # force data from the CSV file

# Number of steps (based on the length of the time data)
num_steps = len(time)

# Initial conditions
z_0 = 0  # initial position (m)
v_0 = 0  # initial velocity (m/s)

# Arrays to store position, velocity, and force
z = np.zeros(num_steps)
v = np.zeros(num_steps)
force = np.zeros(num_steps)

# Set initial conditions
z[0] = z_0
v[0] = v_0

# Simulate the behavior of the object in a viscous fluid with spring constant (force-driven position update)
for n in range(1, num_steps):
    # Get the force for the current time step
    F_sensor = force_data[n]  # force from the CSV data
    
    # Spring force (restoring force due to contact with the surface)
    F_spring = -k * z[n-1]  # Hooke's law for spring contact (negative because spring resists displacement)
    
    # Calculate acceleration based on the equation of motion
    acceleration = (F_sensor / m) - (b * v[n-1] / m) + F_spring / m
    
    # Update velocity and position using Euler integration
    v[n] = v[n-1] + acceleration * delta_t
    z[n] = z[n-1] + v[n] * delta_t

# Plot the results
plt.figure(figsize=(12, 6))


z= z*1000
time = time/1000
# Plot Position vs Time
plt.subplot(2,1, 2)
plt.plot(time, z, label='Position (mm)', color='blue')
plt.title('Position vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Position (mm)')
plt.grid(True)
plt.legend()

# Plot Force vs Time
plt.subplot(2,1, 1)
plt.plot(time, force_data[:len(time)], label='Force (N)', color='red')
plt.title('Force vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
