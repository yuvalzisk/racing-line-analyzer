import csv
import math 
import matplotlib.pyplot as plt

points = []
with open("BrandsHatch_centerline.csv", "r") as file:
    reader = csv.reader(file)
 
    next(reader)

    for row in reader:
        x = float(row[0])
        y = float(row[1])
        points.append((x,y))

print("Number of points:", len(points))
print("First point:", points[0])


total_distance = 0

for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    total_distance += distance

print("Centerline length:", total_distance)

x1, y1 = points[-1]
x2, y2 = points[0]

closing_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

total_distance += closing_distance

print("Closing distance:", closing_distance)
print("Full centerline length:", total_distance)


x_values = [point[0] for point in points]
y_values = [point[1] for point in points]

plt.plot(x_values, y_values, color="blue", label="Centerline")
plt.axis("equal")
plt.title("Brands Hatch - Centerline")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.legend()
plt.grid(True)
plt.savefig("centerline.png")
plt.close()


raceline_points = []

with open("BrandsHatch_raceline.csv", "r") as file:
    reader = csv.reader(file, delimiter=";")

    next(reader)
    next(reader)
    next(reader)

    for row in reader:
        x = float(row[1])
        y = float(row[2])

        raceline_points.append((x, y))

print("Raceline points:", len(raceline_points))
print("First Raceline point:", raceline_points[0])



raceline_x = [point[0] for point in raceline_points]
raceline_y = [point[1] for point in raceline_points]

plt.plot(x_values, y_values, color="blue", label="Centerline")
plt.plot(raceline_x, raceline_y, color="red", label="Raceline")

plt.axis("equal")
plt.title("Brands Hatch - Centerline vs Raceline")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.legend()
plt.grid(True)

plt.savefig("track_comparison.png")
plt.close()



def calculate_curvature(points):
    curvatures = []

    # Remove duplicate closing point if it exists
    if points[0] == points[-1]:
        points = points[:-1]

    n = len(points)

    for i in range(n):
        previous = points[(i - 1) % n]
        current = points[i]
        following = points[(i + 1) % n]

        angle1 = math.atan2(
            current[1] - previous[1],
            current[0] - previous[0]
        )

        angle2 = math.atan2(
            following[1] - current[1],
            following[0] - current[0]
        )

        # Normalize angle difference to [-pi, pi]
        delta_angle = math.atan2(
            math.sin(angle2 - angle1),
            math.cos(angle2 - angle1)
        )

        distance1 = math.dist(previous, current)
        distance2 = math.dist(current, following)

        average_distance = (distance1 + distance2) / 2

        if average_distance == 0:
            curvature = 0
        else:
            curvature = delta_angle / average_distance

        curvatures.append(curvature)

    return curvatures



centerline_curvature = calculate_curvature(points)
raceline_curvature = calculate_curvature(raceline_points)

print("\n--- Curvature Analysis ---")

print("Centerline maximum curvature:",
      max(abs(k) for k in centerline_curvature))

print("Raceline maximum curvature:",
      max(abs(k) for k in raceline_curvature))

print("Centerline average curvature:",
      sum(abs(k) for k in centerline_curvature) / len(centerline_curvature))

print("Raceline average curvature:",
      sum(abs(k) for k in raceline_curvature) / len(raceline_curvature))



def get_progress(points):
    if points[0] == points[-1]:
        points = points[:-1]

    distances = [0]

    for i in range(1, len(points)):
        segment = math.dist(points[i - 1], points[i])
        distances.append(distances[-1] + segment)

    total = distances[-1] + math.dist(points[-1], points[0])

    return [100 * d / total for d in distances]


center_progress = get_progress(points)
race_progress = get_progress(raceline_points)

plt.figure(figsize=(12, 5))

plt.plot(
    center_progress,
    [abs(k) for k in centerline_curvature],
    label="Centerline",
    color="blue"
)

plt.plot(
    race_progress,
    [abs(k) for k in raceline_curvature],
    label="Raceline",
    color="red"
)

plt.xlabel("Lap Progress (%)")
plt.ylabel("Absolute Curvature (1/m)")
plt.title("Brands Hatch - Curvature Comparison")
plt.legend()
plt.grid(True)

plt.savefig("curvature_comparison.png")
plt.close()
