import random, math
import matplotlib.pyplot as plt
import numpy as np



def sample_from_distribution(mu):
    val = random.random()
    #print val,
    if val <= mu:
        return 1
    else:
        return 0


print "mu1:",
mu1 = input()
print "mu2:",
mu2 = input()

eta = 0.0085
total_time = 10000
N = 100

cum_loss = np.zeros(2)
exp3_regret = np.zeros((total_time, N))
exp3_num_op_arms = np.zeros((total_time, N))
iterations = [0] * total_time
best_mu = max(mu1, mu2)



for it in range(N):
    total_reward = 0
    total_best_reward = 0
    cum_loss.fill(0.0)

    for t in range(total_time):
        #eta = math.sqrt(2*math.log(2) / (total_time*2))
        #print np.exp(eta * cum_loss)
        p = np.exp(eta * cum_loss) / np.sum(np.exp(eta * cum_loss))
        #print p
        arm_num = sample_from_distribution(p[0])
        #print arm_num
        if arm_num == 1:
            new_sample = sample_from_distribution(mu1)
            cum_loss[0] += (new_sample) / p[0]
            #print arm_num
            if t == 0:
                exp3_num_op_arms[t][it] = 1
            else:
                exp3_num_op_arms[t][it] = exp3_num_op_arms[t-1][it] + 1
            total_best_reward += new_sample
        else:
            new_sample = sample_from_distribution(mu2)
            cum_loss[1] += new_sample / p[1]
            if t == 0:
                exp3_num_op_arms[t][it] = 0
            else:
                exp3_num_op_arms[t][it] = exp3_num_op_arms[t-1][it]
            total_best_reward += sample_from_distribution(mu1)

        total_reward += new_sample
        exp3_regret[t][it] = total_best_reward - total_reward
        iterations[t] = t
        if t%9999 == 0:
            print t, exp3_num_op_arms[t][it], exp3_regret[t][it], p



avg_exp3_regret = [0] * total_time
std_regret = [0] * total_time
for i in range(total_time):
    #print i, exp3_regret[i]
    avg_exp3_regret[i] = np.average(exp3_regret[i])
    std_regret[i] = np.std(exp3_regret[i]/10)
    if i%100 != 0:
        std_regret[i] = 0
    if i % 1000 == 0:
        print avg_exp3_regret[i], i, type(avg_exp3_regret), len(avg_exp3_regret)


exp3_avg_op_arms = [0] * total_time
std_op_arms = [0] * total_time
for i in range(total_time):
    exp3_avg_op_arms[i] = np.average( exp3_num_op_arms[i] ) / (i+1)
    std_op_arms[i] = np.std(exp3_num_op_arms[i])/(10*(i+1))
    if i%100 != 0:
        std_op_arms[i] = 0
    if i % 1000 == 0:
        print exp3_avg_op_arms[i], i

plt.errorbar(iterations, avg_exp3_regret, yerr=std_regret, label='EXP3')
plt.xlabel('Iterations')
plt.ylim([0,350])
plt.ylabel('Regret')
plt.legend()
plt.show()


plt.errorbar(iterations, exp3_avg_op_arms, yerr=std_op_arms, label='EXP3')
plt.xlabel('Iterations')
plt.ylim([0.5,1])
plt.ylabel('Rate of Optimal Arms')
plt.legend()
plt.show()
