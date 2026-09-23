import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. Inclui o arquivo de launch padrão do Gazebo Classic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    )

    # 2. Caminho absoluto do seu arquivo URDF. 
    # SUBSTITUA ESTE CAMINHO PELO LOCAL ONDE SALVOU SEU ARQUIVO .urdf
    urdf_path = '/home/derico/Atividade2/my_robot.urdf'

    # Lê o conteúdo do arquivo URDF
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # 3. Nó do Robot State Publisher (Lê o modelo e publica no ROS)
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 4. Nó para invocar o robô dentro do Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot'],
        output='screen'
    )

    # 5. Inicializar o publicador dos estados das juntas
    load_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    # 6. Inicializar o controlador Diff Drive (Movimentação)
    load_diff_drive_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        load_joint_state_broadcaster,
        load_diff_drive_controller
    ])
