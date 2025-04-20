# What RRT has?
# RRT has list of obstacles
#     Each obstacle takes a point, and gives if its blockaded
# RRT has a start and goal
#    Each start and goal is a point

import numpy as np

import drawing
import test_data

# RRT (Rapidly-exploring Random Tree) algorithm implementation
class RRT:
    class Node:
        def __init__(self, point, parent):
            self.point = point
            self.parent = parent
            self.children = []
            self.length = self.parent.length + 1 if parent else 0

    def __init__(self, 
                 start, 
                 goal, 
                 obstacle_list, 
                 rand_point_generator,
                 expand_distance=0.5, 
                 robot_radius=.5
                 ):

        self.start = start
        self.goal = goal
        self.obstacle_list = obstacle_list
        self.rand_point_generator = rand_point_generator
        self.expand_distance = expand_distance
        self.robot_radius = robot_radius

        # Initialize the tree with the start point
        self.nodes = [
            self.Node(point=start, parent=None)
        ]
        self.goal_nodes = []
        self.goal_reached = False

    def plan(self, max_iter=1000, quit_once_found=True):
        for i in range(max_iter):
            while True:
                rand_point = self.rand_point_generator()
                nearest_node = self.get_nearest_node(rand_point)
                direction = (rand_point - nearest_node.point)
                direction = direction / np.linalg.norm(direction)  # Normalize the direction vector
                next_point = nearest_node.point + self.expand_distance * direction
            
                # Check if the next point is valid (not in an obstacle)
                if not self.is_valid_point(next_point):
                    continue
                break

            # Expand tree by adding the next_point
            new_node = self.expand_tree(nearest_node, next_point)

            # check if the goal is reached
            if self.is_goal_reached(next_point):
                self.goal_nodes.append(new_node)
                self.goal_reached = True
                if quit_once_found:
                    break
        return self.get_path()
    
    def is_goal_reached(self, point):
        # Check if the point is within a certain distance from the goal
        return np.linalg.norm(point - self.goal) < self.robot_radius
    
    def get_nearest_node(self, point):
        # Find the nearest node in the tree to the given point
        nearest_node = None
        min_distance = float('inf')
        for node in self.nodes:
            distance = np.linalg.norm(node.point - point)
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        return nearest_node
    
    def is_valid_point(self, point):
        # Check if the point is inside any of the obstacles
        for obstacle in self.obstacle_list:
            if obstacle.is_inside(point[0], point[1]):
                return False
        return True
    
    def expand_tree(self, nearest_node, next_point):
        # Create a new node and add it to the tree
        new_node = self.Node(next_point, nearest_node)
        nearest_node.children.append(new_node)
        self.nodes.append(new_node)
        return new_node
    
    def get_path(self):
        # Backtrack from the goal node to get the path
        if not self.goal_nodes:
            return None
        
        # find shortest node
        best_goal_node = min(self.goal_nodes, key=lambda node: node.length)

        path = []
        node = best_goal_node
        while node is not None:
            path.append(node.point)
            node = node.parent
        return np.array(path[::-1])
        # [::-1] reverses the list to get the path from start to goal

def get_sampler_from_obstacles(obstacle_list):
    """
    Returns a function that generates random points in the free space.
    :param obstacle_list: List of obstacles (ellipses)
    :return: Function that generates random points
    """
    import random

    def rand_point():
        while True:
            x = random.uniform(0, 7)
            y = random.uniform(0, 7)
            point = np.array((x, y))
            if all(not obstacle.is_inside(x, y) for obstacle in obstacle_list):
                return point

    return rand_point

    
if __name__ == '__main__':
    obstacle_list, start, goal = test_data.get_obstacles_list()
    # path = test_data.get_path()
    import matplotlib.pyplot as plt

    expand_distance = 0.5
    max_iter = 1000
    rrt = RRT(
        start=start,
        goal=goal,
        obstacle_list=obstacle_list,
        rand_point_generator=get_sampler_from_obstacles(obstacle_list),
        expand_distance=expand_distance,
    )
    path = rrt.plan(max_iter=max_iter, quit_once_found=True)
    print("Path found:", path)


    # Draw the obstacles, start and goal points, and the path
    drawing.draw_graphs(rrt)
    drawing.draw_obstacles(obstacle_list, start, goal, path)
    plt.show()

