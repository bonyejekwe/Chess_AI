
# performance.py: model the performance of the AI

from game import run_game


def simulation(n, m1="random", m2="random", no_draws=True):
    """Run a simulation of n games between AI mode m1 and AI mode m2. Can include or exclude draws"""
    winners = [run_game(2, m1, m2) for _ in range(n)]  # run the game n times and add results to list
    print(f'All results for {n} games b/w {m1} and {m2}: {winners}')
    if no_draws:
        winners = [r for r in winners if r != -5]
        print(f'Without draws: {winners}')
    return winners


#simulation(7, m1="medium")
simulation(1)