import numpy as np
import matplotlib.pyplot as plt

# Define constants
g = 10  # Gravitational acceleration (m/s²)
C_d = 0.5  # Drag coefficient
r_earth = 6371000  # Radius of Earth in meters
rho_0 = 1.225  # Sea level air density in kg/m³
scale_height = 8500  # Scale height for atmosphere in meters
M_e = 6e24 # Earth mass
G = 6.7e-11 # Gravity constant

# Initial conditions
m_0 = 20e3  # Initial mass of the rocket (kg)
m_f = 200e3  # Initial mass of fuel (kg)
m = m_0 + m_f # initial mass
v = np.array([7900, 0])
p = np.array([0, float(r_earth) + 70e3])
r_f = 2000  # Fuel burn rate (kg/s)
v_e = 4000  # Exhaust velocity (m/s)
gimbal_angle = 0 # Gimbal angle for the engine
alpha = 0 # angle of attack. positive counter clockwise from vertical -> +++
engine_active = False

# Time settings
dt = 1  # Time step (s)
t_max = 24000  # Maximum simulation time (s)

# Define air density as a function of altitude
def air_density(r):
    altitude = r - r_earth
    return rho_0 * np.exp(-altitude / scale_height)

# Define drag force
def drag_force(r, v):
    return 0.5 * C_d * air_density(r) * v**2

# 2D Rotation matrix (positive angle is counterclockwise)
def rot_mat(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

# Lists to store simulation data
time = []
positions = []
velocities = []
fuel_levels = []

# Simulation loop
t = 0
while t < t_max:

    # Crash condition
    if np.linalg.norm(p) < r_earth:
        break

    if t < 50 and t > 45:
        gimbal_angle = 1
    else:
        gimbal_angle = 0

    # Gravitational force
    F_g = (- p * G * M_e * m)/(np.linalg.norm(p)**3)

    # Compute the drag force
    abs_v = np.linalg.norm(v)
    if abs_v != 0:
        normalized_vel = v / abs_v
        F_d = -normalized_vel * drag_force(np.linalg.norm(p), abs_v)
    else:
        F_d = np.array([0, 0])

    # Compute the thrust force
    if m_f > 0 and engine_active:
        F_t = np.array([np.sin(alpha), np.cos(alpha)]) * (r_f * v_e)
        F_t = rot_mat(gimbal_angle) @ F_t
    else:
        F_t = np.array([0, 0])

    # Update velocities
    a = (F_g + F_d + F_t) / m
    v = v + a * dt

    # Update position
    p = p + v * dt

    # Update mass
    if engine_active:
        lost_mass = r_f * dt
        if (m_f - r_f * dt) < 0:
            m_f = 0
        else:
            m_f -= lost_mass

    m = m_0 + m_f

    if t == 300:
        print(f'a = {a}')

    # Store data
    time.append(t)
    positions.append(p)
    velocities.append(v)
    fuel_levels.append(m_f)

    # Increment time
    t += dt

# Plots
plt.figure(figsize=(10, 6))

# Altitude plot
plt.subplot(2, 2, (1, 2))
plt.plot(time, [(np.linalg.norm(p))/1e3 for p in positions], color='blue')
plt.title('Rocket Climb Profile')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (km)')

# Fuel plot
plt.subplot(2, 2, 3)
plt.plot(time, fuel_levels, color='brown')
plt.title('Fuel Level Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Fuel Level (kg)')

# Trajectory plot
plt.subplot(2, 2, 4)
plt.plot([p[0] for p in positions], [p[1] for p in positions], color='red')
plt.title('Trajectory')
plt.xlabel('Horizontal (x)')
plt.ylabel('Vertical (y)')

# Add Earth as a big blue circle
earth = plt.Circle((0, 0), r_earth, color='blue', alpha=0.3)  # Circle with radius r_earth
plt.gca().add_artist(earth)
plt.gca().set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.show()
