#!/bin/python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    # 获取包路径
    package_name = 'onerobot_description'
    package_share_dir = get_package_share_directory(package_name)

    # Xacro 文件路径
    xacro_file = os.path.join(package_share_dir, 'urdf', 'robots', 'onerobot.urdf.xacro')

    # 处理 Xacro 文件转换为 URDF
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = robot_description_config.toxml()

    # 声明 launch 参数（可选，用于动态配置）
    declare_robot_description = DeclareLaunchArgument(
        'robot_description',
        default_value=robot_description,
        description='Robot description from Xacro file'
    )

    # robot_state_publisher 节点：发布机器人描述和关节状态
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': LaunchConfiguration('robot_description')}]
    )

    # joint_state_publisher_gui 节点：提供 GUI 来拖动关节，发出 joint_states 话题
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # rviz2 节点：可视化机器人模型
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', PathJoinSubstitution([FindPackageShare(package_name), 'rviz', 'onerobot_description.rviz'])]  # 可选：指定 RViz 配置文件
    )

    return LaunchDescription([
        declare_robot_description,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
