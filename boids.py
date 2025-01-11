import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree

class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = np.random.randn(2)
        self.acceleration = np.zeros(2)
    
class Flock:
    def __init__(self, n):
        self.boids = [Boid(np.random.rand()*100, np.random.rand()*100) for _ in range(n)]
        self.border = self.create_border()

    def create_border(self):
        border_positions = np.linspace(0.0, 100, 100)
        nulletjes = np.repeat(0.0, 100)
        honderdjes = np.repeat(100,100)
        y_zero = np.column_stack((border_positions, nulletjes))  
        x_zero = np.column_stack((nulletjes, border_positions)) 
        y_hundred = np.column_stack((border_positions, honderdjes)) 
        x_hundred = np.column_stack((honderdjes, border_positions))  

        return np.vstack((y_zero, x_zero, y_hundred, x_hundred))
    

    def apply_rules(self):
        '''
        function applying flocking rules (cohesion, alignment, seperation). 
        Uses a tree to find neirest neighbors, seperates from border and neighbors that are too close. 
        Also, aligns velocity and moves toward midpoint of boids in range. 
        '''
        maxdistance = 17
        mindistance = 1.3
        borderdistance = 13
        puntjes = np.array([boidje.position for boidje in self.boids])
        # border_and_neigh = np.vstack((puntjes,self.border))
        tree_with_border = cKDTree(self.border)
        tree = cKDTree(puntjes)
        for i, boid in enumerate(self.boids):
            #find neighbors that lie within max distance
            neighbors_indices = tree.query_ball_point(boid.position, r=maxdistance)
            neighbors_indices.remove(i)  # Exclude the boid itself

            cohesion = 0
            alignment = 0
            seperation = 0

            # cohesion and alignment
            if neighbors_indices:
                relevant_neighbors = puntjes[neighbors_indices]
                relevant_velocities = [self.boids[j].velocity for j in neighbors_indices]
                midpoint = np.mean(relevant_neighbors, axis=0)
                alignment = np.mean(relevant_velocities, axis=0)
                difference = midpoint - boid.position
                cohesion = (np.linalg.norm(difference)/(maxdistance*2))* (midpoint - boid.position)
            
            # speration (other boids)
            neighbors_too_close = tree.query_ball_point(boid.position, r=mindistance)
            neighbors_too_close.remove(i)
            if neighbors_too_close:
                relevant_neighbors = puntjes[neighbors_too_close]
                too_close_point = np.mean(relevant_neighbors, axis=0)
                difference = boid.position - too_close_point
                if(np.linalg.norm(difference < 0.3)):
                    magnitude = 0.1
                else: 
                    magnitude = np.linalg.norm(difference)
                seperation = difference/magnitude

            # border seperation
            border_too_close = tree_with_border.query_ball_point(boid.position, r=borderdistance)
            if border_too_close:
                border_points = self.border[border_too_close]
                too_close_point = np.mean(border_points, axis=0)
                difference = boid.position - too_close_point
                magnitude = np.linalg.norm(difference)
                if(magnitude < 0.3):
                    magnitude = 0.3
    
                seperation += 2*((difference)/magnitude)
                # cohesion*=magnitude
                # alignment*=magnitude

            boid.acceleration = (1* cohesion + 1.5* alignment + 2* seperation)/4.5
            

    def update(self):
        '''
        function thet iterates over all boids and updates position with the velocity. 
        velocity is updated with acceleration that is calculated with cohesion, alignment and seperation rules
        '''
        self.apply_rules()
        for boid in self.boids:

            # updating positions
            boid.position += boid.velocity
            boid.velocity += boid.acceleration*0.3
            speed_limit = 2.0
            speed = np.linalg.norm(boid.velocity)

            # speed limit
            if speed > speed_limit:
                boid.velocity = (boid.velocity / speed) * speed_limit


            # making sure border conditions are met (not very chique but in case of need)
            if boid.position[0] < 0:
                boid.position[0] = 0
                boid.velocity[0] *= -1
            if boid.position[0] > 100:
                boid.position[0] = 100
                boid.velocity[0] *= -1
            if boid.position[1] < 0:
                boid.position[1] = 0
                boid.velocity[1] *= -1
            if boid.position[1] > 100:
                boid.position[1] = 100
                boid.velocity[1] *= -1


def draw_boids(frame):
    global flock
    ax.clear()  # Clear the previous frame
    ax.set_xlim(0, 100)  # Set x-axis limits
    ax.set_ylim(0, 100)  # Set y-axis limits
    ax.set_title(f"Flocking Behavior (Flock Size {len(flock.boids)})")
    # Update boid positions
    flock.update()

    # Draw boids
    for boid in flock.boids:  # Assuming `flock.boids` contains all boids
        ax.plot(boid.position[0], boid.position[1], 'bo', color="purple") 

flock = Flock(100)
fig, ax = plt.subplots()
animation = FuncAnimation(fig, draw_boids, frames=200, interval=50)
plt.show()