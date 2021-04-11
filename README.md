# About

Python3 implementation of the K-dimentional Tree. Using dictionary as the basic node structure.

# Featrues
## Data member:
- k: dimension of a data point. Default to be 2.
- root: root of the kd tree.
## Member function:
- build(points): build the kd tree based on the given (n, k) dataset 'points'.
- nearest_neighbor(point): find the nearest neighbor of the given point 'point' in the dataset. Return 'None" if no such point.
- nearest_neighbor_in_range(center, radius): find the nearest neighbors within the circle with the center 'center' and the radius 'radius'.