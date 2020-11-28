import multi_armed_bandit as mab

from multiprocessing import Pool, cpu_count


def launch_session(n_arms, n_step, n_test):
    # Build environment
    env = mab.BernoulliDynamicBandit(n_arms, prob_of_change=0.002, fixed_action_prob=0.0, save_replay=True)

    # Generate replay
    session = mab.Session(env, [])
    session.run(n_step=n_step)

    # Build Agents
    '''
    discounted_ts = mab.DiscountedBernoulliTS(n_arms, gamma=0.98)
    agents = [discounted_ts]
    
    sw_ts = mab.BernoulliSlidingWindowTS(n_arms, n=75)
    agents = [sw_ts]
    
    max_dsw_ts = mab.MaxDSWTS(n_arms, gamma=0.98, n=20)
    agents = [max_dsw_ts]
    
    min_dsw_ts = mab.MinDSWTS(n_arms, gamma=0.98, n=20)
    agents = [min_dsw_ts]
    '''
    mean_dsw_ts = mab.MeanDSWTS(n_arms, gamma=0.98, n=20)
    agents = [mean_dsw_ts]

    # Build Env with replay
    replay_env = mab.BernoulliReplayBandit(replay=env.get_replay())

    # Build session
    replay_session = mab.Session(replay_env, agents)

    # Run session
    replay_session.run(n_step=n_step, n_test=n_test, use_replay=True)
    results = {agent: replay_session.get_reward_sum(agent)/n_step for agent in agents}
    results.update({"Oracle" : replay_session.get_reward_sum("Oracle")/n_step})
    return results


if __name__ == "__main__": 
    n_arms = 5
    n_step = 1000
    n_test = 30
    n_envs = 50

    rewards = {"Oracle": 0,
                "Thompson Sampling Bernoulli": 0,
                "Discounted Thompson Sampling Bernoulli": 0,
                "Sliding Window Thompson Sampling Bernoulli": 0,
                "Max d-sw TS Bernoulli": 0,
                "Min d-sw TS Bernoulli": 0,
                "Mean d-sw TS Bernoulli":0
                }

    parms = [(n_arms, n_step, n_test) for _ in range(n_envs)]

    pool = Pool(cpu_count())
    results = pool.starmap(launch_session, parms)
    pool.close()
    pool.join()

    for result in results:
        for agent in result:
            rewards[str(agent)] += result[agent]

    print(rewards)