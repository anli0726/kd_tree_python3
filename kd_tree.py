import numpy as np
import pprint
import matplotlib.pyplot as plt

np.random.seed(0)
pp = pprint.PrettyPrinter(indent=4)

class KDTree:
    def __init__(self, k: int = 2):
        self.root = None
        self.k = k

    def build(self, pts):
        self.root = KDTree._build(pts, self.k)

    @staticmethod
    def _build(pts, k, depth: int = 0):
        n = pts.shape[0]
        if n <= 0:
            return
        # print(f"depth = {depth}, axis = {depth % k}, pts = \n{pts}")
        order = np.argsort(pts[:,depth % k], axis=0)
        # print(f"order = {order}")
        sorted_pts = pts[order]
        return {"right": KDTree._build(sorted_pts[n//2+1:], k, depth+1),
                "point": sorted_pts[n//2],
                "left": KDTree._build(sorted_pts[:n//2], k, depth+1)}

    def nearest_neighbor(self, point):
        return KDTree._nn(point, self.root, self.k)

    def nearest_neighbors_in_range(self, center, raidus):
        return np.array(KDTree._nns_in_r([], center, raidus, self.root, self.k))
    
    @staticmethod
    def _compare(pivot, p1, p2):
        if p1 is None: return p2
        if p2 is None: return p1
        if np.linalg.norm(pivot - p1) < np.linalg.norm(pivot - p2):
            return p1
        else:
            return p2
    
    @staticmethod
    def _nn(pt, root, k, depth: int = 0):
        if root is None:
            return None

        axis = depth % k
        next_branch = None
        opposite_branch = None

        if pt[..., axis] < root["point"][..., axis]:
            next_branch = root["left"]
            opposite_branch = root["right"]
        else:
            next_branch = root["right"]
            opposite_branch = root["left"]

        res = KDTree._compare(pt, root["point"], KDTree._nn(pt, next_branch, depth+1))
        '''
        if the distance from the current best to the pt 
        is bigger than the distance from the pt to the spliting boundary
        -> a circle wich can also cover the opposite branch
        '''
        if np.linalg.norm(res - pt) > abs(pt[..., axis] - root["point"][..., axis]): 
            res = KDTree._compare(pt, res, KDTree._nn(pt, opposite_branch, depth+1))
        
        return res

    @staticmethod
    def _nns_in_r(res, center, r, root, k, depth: int = 0):
        if root is None:
            return
        axis = depth % k
        d = np.linalg.norm(root["point"] - center)
        if root["point"][..., axis] <= center[..., axis] - r:    
            print(f"point = {root['point']}, d = {d}, res = {res}, check axis-{axis} >= {root['point'][..., axis]}")
            KDTree._nns_in_r(res, center, r, root["right"], k, depth+1)
        elif center[..., axis] + r <= root["point"][..., axis]:
            print(f"point = {root['point']}, d = {d}, res = {res}, check axis-{axis} <= {root['point'][..., axis]}")
            KDTree._nns_in_r(res, center, r, root["left"], k, depth+1)
        else:
            if d <= r:
                res.append(root["point"])
            print(f"point = {root['point']}, d = {d}, res = {res}, check left & right")
            KDTree._nns_in_r(res, center, r, root["right"], k, depth+1)
            KDTree._nns_in_r(res, center, r, root["left"], k, depth+1)
            
        return res

    def show(self):
        pp.pprint(self.root)


def genereate_2D_int_pts(num_pts: int = 10, low: int = 0, high: int = 10):
    x = np.random.randint(low, high, (num_pts, 1))
    y = np.random.randint(low, high, (num_pts, 1))
    return np.concatenate((x, y), axis=1)

def genereate_2D_float_pts(num_pts: int = 10, factor: int = 10):
    return factor * np.random.random((num_pts, 2))

if __name__ == "__main__":
    pts = genereate_2D_float_pts(20)
    print(pts)
    tree = KDTree()
    tree.build(pts)
    tree.show()
    center = np.array([6,6])
    r = 2
    pts_in_range = tree.nearest_neighbors_in_range(center, r)
    print(pts_in_range)
    if len(pts_in_range) > 0:
        fig, ax = plt.subplots()
        ax.scatter(center[0], center[1], c="g")
        ax.scatter(pts[:, 0], pts[:, 1])
        ax.scatter(pts_in_range[:, 0], pts_in_range[:, 1], c="r")
        circle = plt.Circle(center, r, fill=False)
        ax.add_artist(circle)
        plt.show()
    else: 
        print("no points in range")
