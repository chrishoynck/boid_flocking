

# Flocking Simulation with Boids
By Chris Hoynck van Papendrecht 15340791
## Overview

This program simulates the flocking behavior of boids (artificial agents) in a 2D environment. The simulation demonstrates how simple rules—**cohesion**, **alignment**, and **separation**—can result in complex group behavior resembling bird flocks. The boids also avoid boundaries using a repulsion mechanism.

---

## Features

1. **Flocking Rules**:
   - **Cohesion**: Boids steer toward the midpoint of their neighbors.
   - **Alignment**: Boids align their velocity with nearby neighbors.
   - **Separation**: Boids avoid getting too close to others or the border.
   
2. **Boundary Handling**:
   - Boids bounce off the edges of the simulation space.

3. **Visualization**:
   - Boids are visualized as moving points in a 2D plot.

4. **Customizable Parameters**:
   - Number of boids in the flock.
   - Maximum speed and boundary repulsion strength.

---

## How to Run

1. Ensure you have the required libraries installed:
   ```bash
   pip install numpy matplotlib scipy
   ```

2. Save the program to a Python file, e.g., `boid.py`.

3. Run the program:
   ```bash
   python boid.py
   ```

---

## Notes

1. **Behavior Formation**: 
   - The boids take a few seconds of simulation to organize and demonstrate clear flocking behavior.
   
2. **Parameters**:
   - You can adjust the number of boids by changing (change 100 to desired number of boids):
     ```python
     flock = Flock(100)  
     ```
   - Modify the flocking and boundary rules by tweaking weights in the `apply_rules()` method.

---

## Program Components

### 1. **Boid Class**
   - Represents an individual boid with:
     - Position
     - Velocity
     - Acceleration

### 2. **Flock Class**
   - Manages the flock of boids.
   - Implements rules for movement and interactions:
     - Cohesion, alignment, separation, and border repulsion.
   - Updates positions and ensures boids remain within bounds.

### 3. **Visualization**
   - Real-time animation using `matplotlib.animation.FuncAnimation`.

