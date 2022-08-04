import gym

# kwargs overwrites configs defined in commonroad_rl/gym_commonroad/configs.yaml
env = gym.make("commonroad-v1",
             action_configs={"action_type": "continuous"},
             goal_configs={"observe_distance_goal_long": True,
                           "observe_distance_goal_lat": True},
             surrounding_configs={"observe_lidar_circle_surrounding": True,
                                  "lidar_circle_num_beams": 20},
             reward_type="sparse_reward",
             reward_configs_sparse={"reward_goal_reached": 50.,
                                    "reward_collision": -100.})

observation = env.reset()
for _ in range(500):
  # env.render() # rendered images with be saved under ./img
  action = env.action_space.sample() # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)

  if done:
      observation = env.reset()
env.close()