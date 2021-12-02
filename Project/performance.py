
# performance.py: model the performance of the AI

from game import run_game
import time


def simulation(n, m1="random", m2="random", no_draws=True):
    """Run a simulation of n games between AI mode m1 and AI mode m2. Can include or exclude draws"""
    s = time.time()
    winners = [run_game(2, m1, m2) for _ in range(n)]  # run the game n times and add results to list
    print(f'All results for {n} games b/w {m1} and {m2}: {winners}')
    if no_draws:
        winners = [r for r in winners if r != -5 and r != 0]
        print(f'Without draws: {winners}')
    f = time.time()
    runtime = round((f - s), 2)
    avg_runtime = round(((f - s) / n), 2)
    print(f"Time to run: {runtime} seconds.")
    print(f"Game average time: {avg_runtime} seconds.")
    return winners, runtime, avg_runtime


# l = simulation(1)
s1 = simulation(25, m1="random", m2='random')
#s2 = simulation(9, m1="random", m2='medium')

#s3 = simulation(9, m1="basic", m2='random')
#s4 = simulation(9, m1="medium", m2='random')


print(s1[0])
print(s1[1])
print(s1[2])

"""
print(s2[0])
print(s2[1])
print(s2[2])

print(s3[0])
print(s3[1])
print(s3[2])

print(s4[0])
print(s4[1])
print(s4[2])
"""