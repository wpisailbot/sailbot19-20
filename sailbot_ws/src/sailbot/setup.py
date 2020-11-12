from setuptools import setup
from glob import glob

package_name = 'sailbot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
	('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='njeusman',
    maintainer_email='nick.eusman@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pin_io = sailbot.pin_io:main',
            'control_system = sailbot.control_system:main',
	    'teensy_comms = sailbot.teensy_comms:main',
        ],
    },
)
