import random
import numpy as np
import matplotlib.pyplot as plt


print "mu1:",
mu1 = input()
print "mu2:",
mu2 = input()

epsilon = 0.01
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


regret = np.zeros((total_time, N))
num_op_arms = np.zeros((total_time, N))
iterations = [0] * total_time
best_mu = max(mu1, mu2)

for it in range(N):
    mu1_cur = 0
    mu2_cur = 0
    t1_cur = 0
    t2_cur = 0
    total_reward = 0
    total_best_reward = 0

    for t in range(total_time):
        explore = sample_from_distribution(epsilon)
        if explore == 1:
            if mu1_cur < mu2_cur:
                new_sample = sample_from_distribution(mu1)
                mu1_cur = (mu1_cur * t1_cur + new_sample) * 1.0 / (t1_cur + 1)
                if t == 0:
                    num_op_arms[t][it] = 1
                else:
                    num_op_arms[t][it] = num_op_arms[t-1][it] + 1
                t1_cur += 1
                total_best_reward += new_sample
            else:
                new_sample = sample_from_distribution(mu2)
                mu2_cur = (mu2_cur * t2_cur + new_sample) * 1.0 / (t2_cur + 1)
                if t == 0:
                    num_op_arms[t][it] = 0
                else:
                    num_op_arms[t][it] = num_op_arms[t-1][it]
                t2_cur += 1
                total_best_reward += sample_from_distribution(mu1)
        else:
            if mu1_cur > mu2_cur:
                new_sample = sample_from_distribution(mu1)
                mu1_cur = (mu1_cur * t1_cur + new_sample) * 1.0 / (t1_cur + 1)
                if t == 0:
                    num_op_arms[t][it] = 1
                else:
                    num_op_arms[t][it] = num_op_arms[t-1][it] + 1
                t1_cur += 1
                total_best_reward += new_sample
            else:
                new_sample = sample_from_distribution(mu2)
                mu2_cur = (mu2_cur * t2_cur + new_sample) * 1.0 / (t2_cur + 1)
                if t == 0:
                    num_op_arms[t][it] = 0
                else:
                    num_op_arms[t][it] = num_op_arms[t-1][it]
                t2_cur += 1
                total_best_reward += sample_from_distribution(mu1)

        total_reward += new_sample
        regret[t][it] = total_best_reward - (total_reward * 1.0)
        iterations[t] = t
        if t%9999  == 0:
            print regret[t][it], iterations[t], "mu1_cur", mu1_cur, "mu2_cur", mu2_cur, num_op_arms[t][it], num_op_arms[t][it] / (t+1)




avg_regret = [0] * total_time
std_regret = [0] * total_time
for i in range(total_time):
    #print i, regret[i]
    avg_regret[i] = np.average(regret[i])
    std_regret[i] = np.std(regret[i])/2
    if i%100 != 0:
        std_regret[i] = 0
    if i % 1000 == 0:
        print avg_regret[i], i, regret[i]


avg_op_arms = [0] * total_time
std_op_arms = [0] * total_time
for i in range(total_time):
    avg_op_arms[i] = np.average( num_op_arms[i] ) / (i+1)
    std_op_arms[i] = np.std(num_op_arms[i]/((i+1)))
    if i%100 != 0:
        std_op_arms[i] = 0
    if i % 1000 == 0:
        print avg_op_arms[i], i

plt.errorbar(iterations, avg_regret, yerr=std_regret, label='Epsilon= 0.01')
plt.xlabel('Iterations')
plt.ylim([0,350])
plt.ylabel('Regret')
plt.legend()
plt.show()


plt.errorbar(iterations, avg_op_arms, yerr=std_op_arms, label='avg_op_arms')
plt.xlabel('Iterations')
plt.ylim([0,1])
plt.ylabel('Rate of Optimal Arms')
plt.legend()
plt.show()
