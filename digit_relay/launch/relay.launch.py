from launch import LaunchDescription
from launch_ros.actions import Node

NUM_MEMBERS = 6


def generate_launch_description():
    nodes = [
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen',
        )
    ]

    for member_id in range(1, NUM_MEMBERS + 1):
        nodes.append(
            Node(
                package='digit_relay',
                executable=f'member_{member_id}',
                name=f'member_{member_id}',
                output='screen',
            )
        )

    return LaunchDescription(nodes)
