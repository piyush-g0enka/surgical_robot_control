import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
m = 10  # mass in kg
b = 70  # damping coefficient in N*s/m
k = 1000  # spring constant (N/m)
delta_t = 0.001  # time step in seconds
delay_steps = 30 # Number of steps to introduce as delay (increase this value for more delay)

# Read the data from the CSV file
file_path = 'data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
print(data.head())

# Assuming the CSV contains 'time' and 'force' columns
time = data['time']
time = time/1000
force_data = data['force']

# Initial conditions
z_0 = 0  # initial position (m)
v_0 = 0  # initial velocity (m/s)

# Arrays to store position, velocity, and force
z_desired = np.zeros(len(time))  # Desired position (model output)
z_actual = np.zeros(len(time))  # Actual position (with delay)
v = np.zeros(len(time))  # Velocity
force = np.zeros(len(time))  # Force

# Set initial conditions
z_desired[0] = z_0
z_actual[0] = z_0
v[0] = v_0

# Simulate the system using the contact model (force-driven position update)
for n in range(1, len(time)):
    # Get the force for the current time step
    F_sensor = force_data[n]  # force from the CSV data

    # Spring force (restoring force due to contact with the surface)
    F_spring = -k * z_desired[n-1]  # Hooke's law for spring contact

    # Total force acting on the object
    F_total = F_sensor + F_spring  # combined force

    # Calculate the acceleration using the contact model
    acceleration = (F_total / m) - (b * v[n-1] / m)

    # Update velocity and desired position using Euler integration
    v[n] = v[n-1] + acceleration * delta_t
    z_desired[n] = z_desired[n-1] + v[n] * delta_t

    # Simulate the delay in actual position (lag by 'delay_steps' time steps)
    if n > delay_steps:
        z_actual[n] = z_desired[n - delay_steps]  # lag actual position by 'delay_steps' time steps

# Convert position from meters to millimeters
z_desired_mm = z_desired * 1000  # Desired position in mm
z_actual_mm = z_actual * 1000  # Actual position in mm

# Plot the results
plt.figure(figsize=(12, 6))

# Plot Desired Position vs Time
plt.subplot(2,1, 2)
plt.plot(time, z_desired_mm, label='Desired Position (mm)', color='blue')
plt.plot(time, z_actual_mm, label='Actual Position (mm)', color='green', linestyle='dashed')
plt.title('Desired and Actual Position vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Position (mm)')
plt.grid(True)
plt.legend()

# Plot Force vs Time
plt.subplot(2,1, 1)
plt.plot(time, force_data, label='Force (N)', color='red')
plt.title('Force vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
