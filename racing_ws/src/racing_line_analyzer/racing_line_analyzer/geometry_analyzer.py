import json
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def calculate_length(points):
    # Remove duplicate closing point
    if points[0] == points[-1]:
        points = points[:-1]

    total = 0.0

    for i in range(len(points)):
        total += math.dist(
            points[i],
            points[(i + 1) % len(points)]
        )

    return total


def calculate_curvature(points):
    if points[0] == points[-1]:
        points = points[:-1]

    n = len(points)
    curvatures = []

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

        delta_angle = math.atan2(
            math.sin(angle2 - angle1),
            math.cos(angle2 - angle1)
        )

        distance1 = math.dist(previous, current)
        distance2 = math.dist(current, following)
        average_distance = (distance1 + distance2) / 2

        curvature = (
            delta_angle / average_distance
            if average_distance > 0 else 0.0
        )

        curvatures.append(curvature)

    return curvatures


class GeometryAnalyzer(Node):

    def __init__(self):
        super().__init__('geometry_analyzer')

        self.subscription = self.create_subscription(
            String,
            '/track_data',
            self.process_tracks,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/geometry_results',
            10
        )

        self.get_logger().info('Geometry Analyzer started')

    def process_tracks(self, msg):
        data = json.loads(msg.data)

        results = {}

        for track_name in ['centerline', 'raceline']:
            points = data[track_name]

            length = calculate_length(points)
            curvatures = calculate_curvature(points)

            results[track_name] = {
                'points': points,
                'length': length,
                'curvatures': curvatures,
                'max_curvature': max(abs(k) for k in curvatures),
                'avg_curvature': (
                    sum(abs(k) for k in curvatures)
                    / len(curvatures)
                )
            }

        message = String()
        message.data = json.dumps(results)

        self.publisher.publish(message)

        self.get_logger().info(
            'Geometry analysis completed and published'
        )


def main(args=None):
    rclpy.init(args=args)

    node = GeometryAnalyzer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
