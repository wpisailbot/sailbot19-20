from launch import LaunchDescription
from launch_ros.actions import Node

# Description:
# A launch file that simply launches all nodes

def generate_launch_description():
	return LaunchDescription([
		Node(
			package='sailbot',
			node_executable='pin_io',
			name='pin_io'
		),
		Node(
			package='sailbot',
			node_executable='control_system',
			name='ctrl_sys'
		),
		Node(
			package='sailbot',
			node_executable='teensy_comms',
			name='teensy'
		),
		Node(
			package='sailbot',
			node_executable='debug_interface',
			name='debug'
		)
	])
