from setuptools import find_packages, setup

package_name = 'racing_line_analyzer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yuval',
    maintainer_email='yuval@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'track_publisher = racing_line_analyzer.track_publisher:main',
        'geometry_analyzer = racing_line_analyzer.geometry_analyzer:main',
        'comparison_node = racing_line_analyzer.comparison_node:main',
        'visualizer = racing_line_analyzer.visualizer:main',
    ],
},
)
