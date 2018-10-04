import random, math
import matplotlib.pyplot as plt
import numpy as np


print "mu1:",
mu1 = input()
print "mu2:",
mu2 = input()

alpha = 4
total_time = 10000
N = 100

print mu1, mu2


def sample_from_distribution(mu):
    val = random.random()
    #print val,
    if val <= mu:
        return 1
    else:
        return 0


ucb_regret = np.zeros((total_time, N))
ucb_num_op_arms = np.zeros((total_time, N))
iterations = [0] * total_time
best_mu = max(mu1, mu2)

for it in range(N):
    mu1_cur = 0
    mu2_cur = 0
    t1_cur = 0
    t2_cur = 0
    total_reward = 0
    total_best_reward = 0

    mu1_cur = sample_from_distribution(mu1)
    mu2_cur = sample_from_distribution(mu2)
    t1_cur = 1
    t2_cur = 1

    for t in range(total_time):
        mu1_ucb = mu1_cur + math.sqrt(alpha * math.log(t+1) * 1.0 / (2 * t1_cur))
        mu2_ucb = mu2_cur + math.sqrt(alpha * math.log(t+1) * 1.0 / (2 * t2_cur))
        if mu1_ucb > mu2_ucb:
            new_sample = sample_from_distribution(mu1)
            mu1_cur = (t1_cur * mu1_cur + new_sample) * 1.0 / (t1_cur + 1)
            if t == 0:
                ucb_num_op_arms[t][it] = 1
            else:
                ucb_num_op_arms[t][it] = ucb_num_op_arms[t-1][it] + 1
            t1_cur += 1
            total_best_reward += new_sample
        else:
            new_sample = sample_from_distribution(mu2)
            mu2_cur = (t2_cur * mu2_cur + new_sample) * 1.0 / (t2_cur + 1)
            if t == 0:
                ucb_num_op_arms[t][it] = 0
            else:
                ucb_num_op_arms[t][it] = ucb_num_op_arms[t-1][it]
            t2_cur += 1
            total_best_reward += sample_from_distribution(mu1)

        total_reward += new_sample
        ucb_regret[t][it] = total_best_reward - (total_reward * 1.0)
        iterations[t] = t
        if t%9999 == 0:
            print ucb_regret[t][it], iterations[t], "mu1_cur", mu1_cur, "mu2_cur", mu2_cur, mu1_ucb, mu2_ucb, ucb_num_op_arms[t][it] / (t+1)


avg_ucb_regret = [0] * total_time
std_ucb_regret = [0] * total_time
for i in range(total_time):
    #print i, ucb_regret[i]
    avg_ucb_regret[i] = np.average(ucb_regret[i])
    std_ucb_regret[i] = np.std(ucb_regret[i])
    if i%100 != 0:
        std_ucb_regret[i] = 0
    if i % 1000 == 0:
        print avg_ucb_regret[i], i, type(avg_ucb_regret), len(avg_ucb_regret)


ucb_avg_op_arms = [0] * total_time
std_ucb_op_arms = [0] * total_time
for i in range(total_time):
    ucb_avg_op_arms[i] = np.average( ucb_num_op_arms[i] ) / (i+1)
    std_ucb_op_arms[i] = np.std(ucb_avg_op_arms[i] / (i+1))
    if i % 1000 == 0:
        print ucb_avg_op_arms[i], i

plt.errorbar(iterations, avg_ucb_regret, yerr=std_ucb_regret, label='UCB')
plt.xlabel('Iterations')
plt.ylim([0,100])
plt.ylabel('Regret')
plt.legend()
plt.show()
plt.legend()


plt.errorbar(iterations, ucb_avg_op_arms, yerr=std_ucb_op_arms, label='l1')
plt.xlabel('Iterations')
plt.ylim([0.5,1])
plt.ylabel('Rate of Optimal Arms')
plt.legend()
plt.show()
