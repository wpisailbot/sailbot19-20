from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	return LaunchDescription([
		Node(
			package='sailbot',
			node_executable='pin_io',
			name='pin_io',
			output='screen'
		),
		Node(
			package='sailbot',
			node_executable='control_system',
			name='ctrl_sys',
			output='screen'
		)
	])
