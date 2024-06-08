# Index
1. [Introduction](#introduction)
2. [Physics](#physics)
     - [Gravity Force](#gravity-force)
     - [Drag Force](#drag-force)
     - [Thrust Force](#thrust-force)
5. [Gallery](#gallery)

# Introduction

# Physics

## Gravity Force
The simulator applies the standard newtonian gravity formulation.
Assuming we are only interested in the force acting on the rocket, and that the center of the Earth is in the origin, the gravitational force is:
$$\mathbf{F}_{g} = \frac{G m M_e }{\|\mathbf{r}\|^3}\mathbf{r}$$
Where:
  - G : gravity constant
  - m : mass of the rocket
  - M_e : mass of Earth
  - **r** : position vector of the Rocket w.r.t. the origin

```python
# Gravitational force
F_g = (- p * G * M_e * m)/(np.linalg.norm(p)**3)
```

## Drag force
The drag force is assumed to be a quadratic function of velocity, formulated as:
$$\mathbf{F}_{d} = - \frac{1}{2} C_d \rho \| \mathbf{v} \|^2 \cdot \mathbf{\hat{v}}$$
Where:
  - **v hat** : normalized velocity vector
  - C_d : drag coefficient
  - rho : air density at current altitude
  - |v|: velocity magnitude

If the velocity is 0 the formula is skipped and drag force is also set to 0.
```python
# Compute the drag force
abs_v = np.linalg.norm(v)
if abs_v != 0:
     normalized_vel = v / abs_v
     F_d = -normalized_vel * drag_force(np.linalg.norm(p), abs_v)
else:
     F_d = np.array([0, 0])
```

## Thrust force

# Gallery
<img src="https://i.imgur.com/jhfVVsT.png" width="50%" height="50%" alt="alt text" title="sim">
