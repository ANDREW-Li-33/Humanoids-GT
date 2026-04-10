"""ArticulationCfg for the HighTorque Mini Pi Plus (20 DOF)."""

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

MINI_PI_PLUS_USD_PATH = "/workspace/isaaclab/mini_pi_plus_usd/pi_plus_20dof.usd"


MINI_PI_PLUS_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=MINI_PI_PLUS_USD_PATH,
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=4,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.42),  # ~65cm tall, spawn at roughly half height
        joint_pos={
            # ---- LEFT LEG ----
            "l_hip_pitch_joint": -0.15,     # slight forward lean
            "l_hip_roll_joint": 0.0,
            "l_thigh_joint": 0.0,           # hip yaw
            "l_calf_joint": 0.30,           # knee bend
            "l_ankle_pitch_joint": -0.15,   # compensate for knee
            "l_ankle_roll_joint": 0.0,
            # ---- RIGHT LEG ----
            "r_hip_pitch_joint": -0.15,
            "r_hip_roll_joint": 0.0,
            "r_thigh_joint": 0.0,
            "r_calf_joint": 0.30,
            "r_ankle_pitch_joint": -0.15,
            "r_ankle_roll_joint": 0.0,
            # ---- LEFT ARM ----
            "l_shoulder_pitch_joint": 0.0,
            "l_shoulder_roll_joint": 0.0,
            "l_upper_arm_joint": 0.0,       # shoulder yaw
            "l_elbow_joint": 0.0,
            "l_wrist_joint": 0.0,
            # ---- RIGHT ARM ----
            "r_shoulder_pitch_joint": 0.0,
            "r_shoulder_roll_joint": 0.0,
            "r_upper_arm_joint": 0.0,
            "r_elbow_joint": 0.0,
            "r_wrist_joint": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        # Leg actuators: higher gains, these bear weight
        # effort=20 Nm per URDF
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*hip_pitch_joint", ".*hip_roll_joint",
                ".*thigh_joint",
                ".*calf_joint",
                ".*ankle_pitch_joint", ".*ankle_roll_joint",
            ],
            stiffness={
                ".*hip_pitch_joint": 60.0,
                ".*hip_roll_joint": 40.0,
                ".*thigh_joint": 40.0,       # hip yaw
                ".*calf_joint": 60.0,        # knee
                ".*ankle_pitch_joint": 40.0,
                ".*ankle_roll_joint": 30.0,
            },
            damping={
                ".*hip_pitch_joint": 6.0,
                ".*hip_roll_joint": 4.0,
                ".*thigh_joint": 4.0,
                ".*calf_joint": 6.0,
                ".*ankle_pitch_joint": 4.0,
                ".*ankle_roll_joint": 3.0,
            },
        ),
        # Arm actuators: lower gains
        # effort=10 Nm per URDF
        "arms": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*shoulder_pitch_joint", ".*shoulder_roll_joint",
                ".*upper_arm_joint",
                ".*elbow_joint",
                ".*wrist_joint",
            ],
            stiffness={
                ".*shoulder.*": 30.0,
                ".*upper_arm_joint": 20.0,
                ".*elbow_joint": 20.0,
                ".*wrist_joint": 10.0,
            },
            damping={
                ".*shoulder.*": 3.0,
                ".*upper_arm_joint": 2.0,
                ".*elbow_joint": 2.0,
                ".*wrist_joint": 1.0,
            },
        ),
    },
)
