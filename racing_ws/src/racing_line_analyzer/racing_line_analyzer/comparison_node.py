import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ComparisonNode(Node):

    def __init__(self):
        super().__init__('comparison_node')

        self.subscription = self.create_subscription(
            String,
            '/geometry_results',
            self.compare_tracks,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/comparison_results',
            10
        )

        self.get_logger().info('Comparison Node started')

    def compare_tracks(self, msg):
        data = json.loads(msg.data)

        center = data['centerline']
        race = data['raceline']

        length_difference = (
            center['length'] - race['length']
        )

        max_curvature_reduction = (
            100 *
            (center['max_curvature'] - race['max_curvature'])
            / center['max_curvature']
        )

        avg_curvature_reduction = (
            100 *
            (center['avg_curvature'] - race['avg_curvature'])
            / center['avg_curvature']
        )

        results = {
            'centerline': center,
            'raceline': race,
            'comparison': {
                'length_difference_m': length_difference,
                'max_curvature_reduction_percent':
                    max_curvature_reduction,
                'avg_curvature_reduction_percent':
                    avg_curvature_reduction
            }
        }

        message = String()
        message.data = json.dumps(results)

        self.publisher.publish(message)

        self.get_logger().info(
            f'Comparison completed: '
            f'length difference = {length_difference:.2f} m, '
            f'max curvature reduction = '
            f'{max_curvature_reduction:.2f}%'
        )


def main(args=None):
    rclpy.init(args=args)

    node = ComparisonNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
