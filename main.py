import math
import matplotlib.pyplot as plt

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def brute_force(points):
    min_dist = float('inf')
    p1, p2 = None, None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if d < min_dist:
                min_dist = d
                p1, p2 = points[i], points[j]
    return p1, p2, min_dist

def closest_split_pair(points_sorted_by_x, points_sorted_by_y, delta, best_pair):
    mid_x = points_sorted_by_x[len(points_sorted_by_x) // 2][0]
    in_strip = [p for p in points_sorted_by_y if mid_x - delta <= p[0] <= mid_x + delta]

    best = delta
    ln_in_strip = len(in_strip)

    for i in range(ln_in_strip):
        for j in range(i + 1, min(i + 7, ln_in_strip)):
            p, q = in_strip[i], in_strip[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = (p, q)
                best = dst

    return best_pair[0], best_pair[1], best

def closest_pair_recursive(points_sorted_by_x, points_sorted_by_y, depth=0, ax=None):
    num_points = len(points_sorted_by_x)

    if num_points <= 3:
        return brute_force(points_sorted_by_x)

    mid = num_points // 2
    midpoint = points_sorted_by_x[mid]

    left_sorted_by_x = points_sorted_by_x[:mid]
    right_sorted_by_x = points_sorted_by_x[mid:]

    midpoint_x = midpoint[0]
    left_sorted_by_y = list(filter(lambda x: x[0] <= midpoint_x, points_sorted_by_y))
    right_sorted_by_y = list(filter(lambda x: x[0] > midpoint_x, points_sorted_by_y))

    (p1_left, p2_left, min_dist_left) = closest_pair_recursive(left_sorted_by_x, left_sorted_by_y, depth + 1, ax)
    (p1_right, p2_right, min_dist_right) = closest_pair_recursive(right_sorted_by_x, right_sorted_by_y, depth + 1, ax)

    if min_dist_left < min_dist_right:
        min_dist = min_dist_left
        closest_pair = (p1_left, p2_left)
    else:
        min_dist = min_dist_right
        closest_pair = (p1_right, p2_right)

    possible_closest_pair = closest_split_pair(points_sorted_by_x, points_sorted_by_y, min_dist, closest_pair)

    # Візуалізація
    if ax is not None:
        ax.plot([midpoint_x, midpoint_x], [0, 10], 'k--', lw=1)
        ax.scatter([p1_left[0], p2_left[0]], [p1_left[1], p2_left[1]], c='blue')
        ax.scatter([p1_right[0], p2_right[0]], [p1_right[1], p2_right[1]], c='red')

    return possible_closest_pair

def closest_pair(points, ax=None):
    points_sorted_by_x = sorted(points, key=lambda x: x[0])
    points_sorted_by_y = sorted(points, key=lambda x: x[1])
    p1, p2, min_dist = closest_pair_recursive(points_sorted_by_x, points_sorted_by_y, ax=ax)
    return p1, p2, min_dist

# Тестовий приклад
points = [(0, 3), (1, 1), (2, 2), (3, 3), (5, 1), (6, 0), (7, 4), (8, 2), (9, 6)]

fig, ax = plt.subplots()
ax.set_xlim(-1, 10)
ax.set_ylim(-1, 7)
ax.scatter(*zip(*points))

p1, p2, min_dist = closest_pair(points, ax=ax)
print(f"The closest pair of points are {p1} and {p2} with a distance of {min_dist}")

ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], c='green')
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-')

plt.show()