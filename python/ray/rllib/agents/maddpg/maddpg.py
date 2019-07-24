from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ray.rllib.agents.trainer import with_common_config
from ray.rllib.agents.dqn.dqn import GenericOffPolicyTrainer
from ray.rllib.agents.maddpg.maddpg_policy import MADDPGTFPolicy
from ray.rllib.optimizers import MultiAgentSyncReplayOptimizer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# yapf: disable
# __sphinx_doc_begin__
DEFAULT_CONFIG = with_common_config({
    # === Default algorithm setting ===
    "good_policy": "maddpg",
    "adv_policy": "maddpg",
    "run_id": 0,
    "obs_space_dict": None,
    "act_space_dict": None,

    # === Debugging ===
    "log_level": "ERROR",

    # === Evaluation ===
    # Evaluate with epsilon=0 every `evaluation_interval` training iterations.
    # The evaluation stats will be reported under the "evaluation" metric key.
    # Note that evaluation is currently not parallelized, and that for Ape-X
    # metrics are already only reported for the lowest epsilon workers.
    # NOTE: If this value is set, "batch_mode" is automatically changed into "complete_episodes".
    "evaluation_interval": None,
    # Number of episodes to run per evaluation period.
    "evaluation_num_episodes": 10,

    # === Model ===
    # Apply a state preprocessor with spec given by the "model" config option
    # (like other RL algorithms). This is mostly useful if you have a weird
    # observation shape, like an image. Disabled by default.
    "use_state_preprocessor": False,
    # Postprocess the policy network model output with these hidden layers. If
    # use_state_preprocessor is False, then these will be the *only* hidden
    # layers in the network.
    "actor_hiddens": [64, 64],
    # Hidden layers activation of the postprocessing stage of the policy
    # network
    "actor_hidden_activation": "relu",
    # Postprocess the critic network model output with these hidden layers;
    # again, if use_state_preprocessor is True, then the state will be
    # preprocessed by the model specified with the "model" config option first.
    "critic_hiddens": [64, 64],
    # Hidden layers activation of the postprocessing state of the critic.
    "critic_hidden_activation": "relu",
    # N-step Q learning
    "n_step": 1,

    # === Replay buffer ===
    # Size of the replay buffer. Note that if async_updates is set, then
    # each worker will have a replay buffer of this size.
    "buffer_size": int(1e6),

    # === Optimization ===
    # Learning rate for the critic (Q-function) optimizer.
    "critic_lr": 1e-2,
    # Learning rate for the actor (policy) optimizer.
    "actor_lr": 1e-2,
    # Update the target network every `target_network_update_freq` steps.
    "target_network_update_freq": 0,
    # Update the target by \tau * policy + (1-\tau) * target_policy
    "tau": 0.01,
    # Weights for feature regularization for the actor
    "actor_feature_reg": 0.001,
    # If not None, clip gradients during optimization at this value
    "grad_norm_clipping": 0.5,
    # How many steps of the model to sample before learning starts.
    # NOTE: train_batch_size * max_episode_len
    "learning_starts": 1024 * 25,
    # Update the replay buffer with this many samples at once. Note that this
    # setting applies per-worker if num_workers > 1.
    "sample_batch_size": 100,
    # Size of a batched sampled from replay buffer for training. Note that
    # if async_updates is set, then each worker returns gradients for a
    # batch of this size.
    "train_batch_size": 1024,
    # Number of env steps to optimize for before returning
    # NOTE: For 0 value, 1 (iteration) = sample_batch_size * num_workers * num_envs_per_worker
    # NOTE:                             (timesteps)
    "timesteps_per_iteration": 0,

    # === Parallelism ===
    # Number of workers for collecting samples with. This only makes sense
    # to increase if your environment is particularly slow to sample, or if
    # you're using the Async or Ape-X optimizers.
    "num_workers": 1,
    # Prevent iterations from going lower than this time span
    # NOTE: timesteps/iteration may vary for each iteration if it is positive.
    "min_iter_time_s": 0,
})
# __sphinx_doc_end__
# yapf: enable


def set_global_timestep(trainer):
    global_timestep = trainer.optimizer.num_steps_sampled
    trainer.train_start_timestep = global_timestep


def make_optimizer(workers, config):
    return MultiAgentSyncReplayOptimizer(
        workers,
        learning_starts=config["learning_starts"],
        buffer_size=config["buffer_size"],
        train_batch_size=config["train_batch_size"]
    )


def add_trainer_metrics(trainer, result):
    global_timestep = trainer.optimizer.num_steps_sampled
    result.update(
        timesteps_this_iter=global_timestep - trainer.train_start_timestep,
        info=dict({
            "num_target_updates": trainer.state["num_target_updates"],
        }, **trainer.optimizer.stats()))


def collect_metrics(trainer):
    result = trainer.collect_metrics()
    return result


class CustomStdOut(object):
    def _log_result(self, result):
        if result["training_iteration"] % 50 == 0:
            try:
                print("steps: {}, episodes: {}, mean episode reward: {}, agent episode reward: {}, time: {}".format(
                    result["timesteps_total"],
                    result["episodes_total"],
                    result["episode_reward_mean"],
                    result["policy_reward_mean"],
                    round(result["time_total_s"] - self.cur_time, 3)
                ))
            except:
                pass

            self.cur_time = result["time_total_s"]


MADDPGTrainer = GenericOffPolicyTrainer.with_updates(
    name="MADDPG",
    default_config=DEFAULT_CONFIG,
    default_policy=MADDPGTFPolicy,
    before_init=None,
    before_train_step=set_global_timestep,
    make_policy_optimizer=make_optimizer,
    after_train_result=add_trainer_metrics,
    collect_metrics_fn=collect_metrics,
    before_evaluate_fn=None,
    mixins=[CustomStdOut]
)
