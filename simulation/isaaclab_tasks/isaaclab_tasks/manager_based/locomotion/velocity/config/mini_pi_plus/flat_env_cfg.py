"""Velocity-tracking environment config for Mini Pi Plus biped."""

import math
from isaaclab.utils import configclass
from isaaclab.managers import SceneEntityCfg

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp
from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import (
    LocomotionVelocityRoughEnvCfg,
)
from .mini_pi_plus_cfg import MINI_PI_PLUS_CFG


@configclass
class MiniPiPlusFlatEnvCfg(LocomotionVelocityRoughEnvCfg):
    """Flat-terrain velocity tracking for the Mini Pi Plus."""

    def __post_init__(self):
        super().__post_init__()

        # -- Scene --
        self.scene.robot = MINI_PI_PLUS_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        self.scene.num_envs = 2048
        self.scene.env_spacing = 2.5

        # -- Disable height scanner (references "base", not needed on flat terrain) --
        self.scene.height_scanner = None
        self.observations.policy.height_scan = None

        # -- Simulation: smaller robot needs smaller timestep --
        self.sim.dt = 0.002            # 500 Hz physics
        self.decimation = 10           # 50 Hz policy
        self.sim.render_interval = 20  # 25 Hz render

        # -- Commands: conservative for a 65cm biped --
        self.commands.base_velocity.ranges.lin_vel_x = (-0.3, 0.6)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.2, 0.2)
        self.commands.base_velocity.ranges.ang_vel_z = (-0.5, 0.5)
        self.commands.base_velocity.ranges.heading = (-math.pi, math.pi)

        # -- Actions --
        self.actions.joint_pos.scale = 0.25

        # -- Rewards --
        self.rewards.track_lin_vel_xy_exp.weight = 1.5
        self.rewards.track_ang_vel_z_exp.weight = 0.75
        self.rewards.lin_vel_z_l2.weight = -2.0
        self.rewards.ang_vel_xy_l2.weight = -0.05
        self.rewards.dof_torques_l2.weight = -0.0001
        self.rewards.dof_acc_l2.weight = -2.5e-7
        self.rewards.action_rate_l2.weight = -0.01
        self.rewards.dof_pos_limits.weight = -5.0
        self.rewards.flat_orientation_l2.weight = -5.0

        # Foot contact
        self.rewards.feet_air_time.weight = 0.5
        self.rewards.feet_air_time.params["sensor_cfg"] = SceneEntityCfg(
            "contact_forces", body_names=["l_ankle_roll_link", "r_ankle_roll_link"]
        )
        self.rewards.feet_air_time.params["threshold"] = 0.4

        # Penalize non-foot contacts
        self.rewards.undesired_contacts.weight = -1.0
        self.rewards.undesired_contacts.params["sensor_cfg"] = SceneEntityCfg(
            "contact_forces", body_names=["base_link", ".*thigh_link", ".*calf_link", ".*hip_pitch_link", ".*hip_roll_link"]
        )

        # -- Fix body name: parent config uses "base", ours is "base_link" --
        self.events.add_base_mass = None
        self.events.base_com = None
        self.events.push_robot = None
        self.events.base_external_force_torque.params["asset_cfg"] = SceneEntityCfg("robot", body_names="base_link")
        self.terminations.base_contact.params["sensor_cfg"] = SceneEntityCfg("contact_forces", body_names="base_link")

        # -- No terrain curriculum --
        self.curriculum.terrain_levels = None

        # -- Viewer --
        self.viewer.eye = (3.0, 3.0, 2.0)
        self.viewer.lookat = (0.0, 0.0, 0.3)


@configclass
class MiniPiPlusFlatEnvCfg_PLAY(MiniPiPlusFlatEnvCfg):
    """Evaluation config with fewer envs."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 50
        self.observations.policy.enable_corruption = False
