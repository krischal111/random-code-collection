def draw_obstacles(obstacle_list, start, goal, path=None):
    """
    Draws the obstacles, start and goal points, and the path.
    :param obstacle_list: List of obstacles (ellipses)
    :param start: Start point (x, y)
    :param goal: Goal point (x, y)
    :param path: Path points (N, 2)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # draw obstacles
    for ellipse in obstacle_list:
        theta = np.linspace(0, 2 * np.pi, 100)
        x = ellipse.x0 + ellipse.a * np.cos(theta)
        y = ellipse.y0 + ellipse.b * np.sin(theta)
        plt.plot(x, y)
    plt.xlim(0, 7)
    plt.ylim(0, 7)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()

    # draw path
    if path is not None:
        plt.plot(path[...,0], path[...,1], 'b-', label='Path')
        for i in range(1,len(path) - 1):
            plt.plot(path[i, 0], path[i, 1], 'bo')

    # draw start and goal
    plt.plot(start[0], start[1], 'ro', label='Start')
    plt.plot(goal[0], goal[1], 'yo', label='Goal')
    plt.legend()
    plt.title('RRT Path Planning')


def draw_graphs(rrt):
    """
    Draws the RRT graph.
    :param rrt: RRT object
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # draw obstacles
    for ellipse in rrt.obstacle_list:
        theta = np.linspace(0, 2 * np.pi, 100)
        x = ellipse.x0 + ellipse.a * np.cos(theta)
        y = ellipse.y0 + ellipse.b * np.sin(theta)
        plt.plot(x, y)

    # draw nodes
    for node in rrt.nodes:
        plt.plot(node.point[0], node.point[1], 'go')

    # draw edges
    for node in rrt.nodes:
        if node.parent is not None:
            plt.plot([node.point[0], node.parent.point[0]], [node.point[1], node.parent.point[1]], 'g-')

    plt.xlim(0, 7)
    plt.ylim(0, 7)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()