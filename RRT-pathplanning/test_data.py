
def get_obstacles_list():
    """
    Returns a list of obstacles (ellipses) for the RRT algorithm.
    :return: List of obstacles (StraightEllipse objects)
    """
    import numpy as np

    from geometry import StraightEllipse

    obstacle_list = [
        StraightEllipse(1, 1, 1, 1),
        StraightEllipse(1.5, 1, 2.5, 1),
        StraightEllipse(2, 1, 3, 4),
        StraightEllipse(1.5, 1.5, 5, 4),
    ]
    start = np.array((3, 6))
    goal = np.array((6, 1))
    return obstacle_list, start, goal

def get_path():
    """
    Returns a path for the RRT algorithm.
    :return: Path points (N, 2)
    """
    import numpy as np
    # Path points (N, 2)
    path = [
        [3, 6],
        [2, 6],
        [1, 5],
        [0.5, 4],
        [1, 3],
        [2, 2.5],
        [4, 2],
        [5, 1],
        [6, 1],
    ]
    return np.array(path)
