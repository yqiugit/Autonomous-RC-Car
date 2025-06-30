from setuptools import find_packages, setup

package_name = 'pca9685_control'

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
    maintainer='yusen',
    maintainer_email='20yq21@queensu.ca',
    description='PCA9685 for ESC steering and throttle control',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = pca9685_control.my_node:main',
            'talker = pca9685_control.publisher_member_function:main',
            'listener = pca9685_control.subscriber_member_function:main',
        ],
    },

)
