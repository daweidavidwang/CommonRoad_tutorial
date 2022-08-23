import sys, os
sys.path.append(os.getcwd()+"/commonroad-rl/")
import gym
import commonroad_rl.gym_commonroad

import yaml
import copy

# Read in environment configurations
env_configs = {}
with open("commonroad-rl/commonroad_rl/gym_commonroad/configs.yaml", "r") as config_file:
    env_configs = yaml.safe_load(config_file)["env_configs"]
    
# Change a configuration directly
env_configs["reward_type"] = "dense_reward"

# Save settings for later use
log_path = "tutorials/logs/"
os.makedirs(log_path, exist_ok=True)

with open(os.path.join(log_path, "environment_configurations.yml"), "w") as config_file:
    yaml.dump(env_configs, config_file)

# Read in model hyperparameters
hyperparams = {}
with open("commonroad-rl/commonroad_rl/hyperparams/ppo2.yml", "r") as hyperparam_file:
    hyperparams = yaml.safe_load(hyperparam_file)["commonroad-v1"]
    
# Save settings for later use
with open(os.path.join(log_path, "model_hyperparameters.yml"), "w") as hyperparam_file:
    yaml.dump(hyperparams, hyperparam_file)
    
# Remove `normalize` as it will be handled explicitly later
if "normalize" in hyperparams:
    del hyperparams["normalize"]

import gym
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize

import commonroad_rl.gym_commonroad

# Create a Gym-based RL environment with specified data paths and environment configurations
meta_scenario_path = "scenario/pickle/meta_scenario"
training_data_path = "scenario/pickle/problem"
training_env = gym.make("commonroad-v1", 
                        meta_scenario_path=meta_scenario_path,
                        train_reset_config_path= training_data_path,
                        **env_configs)

# Wrap the environment with a monitor to keep an record of the learning process
info_keywords=tuple(["is_collision", \
                     "is_time_out", \
                     "is_off_road", \
                     "is_friction_violation", \
                     "is_goal_reached"])
training_env = Monitor(training_env, log_path + "0", info_keywords=info_keywords)

# Vectorize the environment with a callable argument
def make_training_env():
    return training_env
training_env = DummyVecEnv([make_training_env])

# Normalize observations and rewards
training_env = VecNormalize(training_env, norm_obs=True, norm_reward=True)

from stable_baselines.common.callbacks import BaseCallback, EvalCallback

# Append the additional key
env_configs_test = copy.deepcopy(env_configs)
env_configs_test["test_env"] = True

# Create the testing environment
testing_data_path = "scenario/pickle/problem"
testing_env = gym.make("commonroad-v1", 
                        meta_scenario_path=meta_scenario_path,
                        test_reset_config_path= testing_data_path,
                        **env_configs_test)

# Wrap the environment with a monitor to keep an record of the testing episodes 
log_path_test = "logs/test"
os.makedirs(log_path_test, exist_ok=True)

testing_env = Monitor(testing_env, log_path_test + "/0", info_keywords=info_keywords)

# Vectorize the environment with a callable argument
def make_testing_env():
    return testing_env
testing_env = DummyVecEnv([make_testing_env])

# Normalize only observations during testing
testing_env = VecNormalize(testing_env, norm_obs=True, norm_reward=False)

# Define a customized callback function to save the vectorized and normalized environment wrapper
class SaveVecNormalizeCallback(BaseCallback):
    def __init__(self, save_path: str, verbose=1):
        super(SaveVecNormalizeCallback, self).__init__(verbose)
        self.save_path = save_path
        
    def _init_callback(self) -> None:
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)
    
    def _on_step(self) -> bool:
        save_path_name = os.path.join(self.save_path, "vecnormalize.pkl")
        self.model.get_vec_normalize_env().save(save_path_name)
        print("Saved vectorized and normalized environment to {}".format(save_path_name))
    
# Pass the testing environment and customized saving callback to an evaluation callback
# Note that the evaluation callback will triggers three evaluating episodes after every 500 training steps
save_vec_normalize_callback = SaveVecNormalizeCallback(save_path=log_path)
eval_callback = EvalCallback(testing_env, 
                             log_path=log_path, 
                             eval_freq=500, 
                             n_eval_episodes=3, 
                             callback_on_new_best=save_vec_normalize_callback)


from stable_baselines import PPO2

# Create the model together with its model hyperparameters and the training environment
model = PPO2(env=training_env, **hyperparams)

# Start the learning process with the evaluation callback
n_timesteps=5000
model.learn(n_timesteps, eval_callback)

model.save("logs/best_model")
model.get_vec_normalize_env().save("logs/vecnormalize.pkl")