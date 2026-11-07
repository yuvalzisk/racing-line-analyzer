
import json
import math
import os

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def lap_progress(points):
    # The last point may duplicate the first
    if points[0] == points[-1]:
        points = points[:-1]

    distances = [0.0]

    for i in range(1, len(points)):
        segment = math.dist(points[i - 1], points[i])
        distances.append(distances[-1] + segment)

    total = distances[-1] + math.dist(
        points[-1], points[0]
    )

    return [100 * d / total for d in distances]


class Visualizer(Node):

    def __init__(self):
        super().__init__('visualizer')

        self.output_dir = os.path.expanduser(
            os.environ.get(
                'OUTPUT_DIR',
                '~/racing-line-analyzer/results'
            )
        )

        os.makedirs(self.output_dir, exist_ok=True)

        self.subscription = self.create_subscription(
            String,
            '/comparison_results',
            self.generate_results,
            10
        )

        self.get_logger().info('Visualizer started')

    def generate_results(self, msg):
        data = json.loads(msg.data)

        center = data['centerline']
        race = data['raceline']

        center_points = center['points']
        race_points = race['points']

        # Graph 1: Track comparison
        plt.figure(figsize=(10, 7))

        plt.plot(
            [p[0] for p in center_points],
            [p[1] for p in center_points],
            label='Centerline',
            color='blue'
        )

        plt.plot(
            [p[0] for p in race_points],
            [p[1] for p in race_points],
            label='Raceline',
            color='red'
        )

        plt.axis('equal')
        plt.xlabel('X (meters)')
        plt.ylabel('Y (meters)')
        plt.title('Brands Hatch - Track Comparison')
        plt.legend()
        plt.grid(True)

        plt.savefig(
            os.path.join(
                self.output_dir, 'track_comparison.png'
            ),
            dpi=150
        )
        plt.close()

        # Graph 2: Curvature comparison
        center_progress = lap_progress(center_points)
        race_progress = lap_progress(race_points)

        plt.figure(figsize=(12, 5))

        plt.plot(
            center_progress,
            [abs(k) for k in center['curvatures']],
            label='Centerline',
            color='blue'
        )

        plt.plot(
            race_progress,
            [abs(k) for k in race['curvatures']],
            label='Raceline',
            color='red'
        )

        plt.xlabel('Lap Progress (%)')
        plt.ylabel('Absolute Curvature (1/m)')
        plt.title('Brands Hatch - Curvature Comparison')
        plt.legend()
        plt.grid(True)

        plt.savefig(
            os.path.join(
                self.output_dir, 'curvature_comparison.png'
            ),
            dpi=150
        )
        plt.close()

        # Summary with numerical results
        summary = {
            'centerline_length_m': center['length'],
            'raceline_length_m': race['length'],
            'centerline_max_curvature':
                center['max_curvature'],
            'raceline_max_curvature':
                race['max_curvature'],
            'centerline_avg_curvature':
                center['avg_curvature'],
            'raceline_avg_curvature':
                race['avg_curvature'],
            **data['comparison']
        }

        with open(
            os.path.join(self.output_dir, 'summary.json'),
            'w'
        ) as file:
            json.dump(summary, file, indent=4)

        self.get_logger().info(
            'Visualization completed. Results saved.'
        )


def main(args=None):
    rclpy.init(args=args)
    node = Visualizer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
