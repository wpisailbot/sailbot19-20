from launch import LaunchDescription
from launch_ros.actions import Node

# Description:
# A launch file that launches all nodes and opens
# different terminal window to display each node's
# callback messages

def generate_launch_description():
	return LaunchDescription([
		# prefix opens new terminal window
		# output displays callback messages in terminal
		Node(
			package='sailbot',
			node_executable='pin_io',
			name='pin_io',
			prefix='gnome-terminal --command',
			output='screen'
		),
		Node(
			package='sailbot',
			node_executable='control_system',
			name='ctrl_sys',
			prefix='gnome-terminal --command',
			output='screen'
		),
		Node(
			package='sailbot',
			node_executable='teensy_comms',
			name='teensy'
		),
		Node(
			package='sailbot',
			node_executable='debug_interface',
			name='debug',
			prefix='gnome-terminal --command',
			output='screen'
		)
	])
