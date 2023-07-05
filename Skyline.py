import numpy as np

# Function to check if a dominates b
def dominates(a, b):
    return np.all(a <= b) and np.any(a < b)

# Function to calculate the probability for a tuple not being dominated by others
def prob_not_dominated(tuple_a, workers_data, worker_a):
    result = 1
    for worker_b in workers_data:
        if np.array_equal(worker_a, worker_b):  # Ignore the same worker
            continue
        count = sum(dominates(b, tuple_a) for b in worker_b)
        result *= 1 - count / len(worker_b)
    return result

# Function to calculate the Ps-score for a worker
def calculate_ps_score(worker_a, workers_data):
    probabilities = [prob_not_dominated(a, workers_data, worker_a) for a in worker_a]
    return np.mean(probabilities)

# Example data
worker_A_data = np.array([(1, 7), (2, 5), (3, 3), (4, 6)])
worker_B_data = np.array([(6, 0.5), (6.5, 1), (7.5, 1.5)])
worker_C_data = np.array([(5, 4), (6, 8), (7, 5.5), (8, 2)])

workers_data = [worker_A_data, worker_B_data, worker_C_data]

# Compute Ps-scores
ps_scores = [calculate_ps_score(worker, workers_data) for worker in workers_data]
print("Ps-scores:", ps_scores)
