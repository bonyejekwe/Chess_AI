
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
    print(f"Time to run: {round((f - s), 2)} seconds.")
    print(f"Game average time: {round(((f - s) / n), 2)} seconds.")
    return winners


# l = simulation(12)
simulation(7, m1="medium", m2='basic')
