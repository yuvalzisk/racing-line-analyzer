import csv
import json
import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TrackPublisher(Node):

    def __init__(self):
        super().__init__('track_publisher')

        self.publisher = self.create_publisher(
            String,
            '/track_data',
            10
        )

        self.data_dir = os.path.expanduser(
        os.environ.get(
        'DATA_DIR',
        '~/racing-line-analyzer'
         )
        )

        self.timer = self.create_timer(
            5.0,
            self.publish_tracks
        )

        self.get_logger().info('Track Publisher started')

    def read_csv(self, filename, delimiter, skip_rows, x_col, y_col):
        points = []

        path = os.path.join(self.data_dir, filename)

        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)

            for _ in range(skip_rows):
                next(reader)

            for row in reader:
                x = float(row[x_col])
                y = float(row[y_col])
                points.append([x, y])

        return points

    def publish_tracks(self):
        centerline = self.read_csv(
            'BrandsHatch_centerline.csv', ',', 1, 0, 1
        )

        raceline = self.read_csv(
            'BrandsHatch_raceline.csv', ';', 3, 1, 2
        )

        data = {
            'centerline': centerline,
            'raceline': raceline
        }

        message = String()
        message.data = json.dumps(data)

        self.publisher.publish(message)

        self.get_logger().info(
            f'Published {len(centerline)} centerline points '
            f'and {len(raceline)} raceline points'
        )


def main(args=None):
    rclpy.init(args=args)

    node = TrackPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
