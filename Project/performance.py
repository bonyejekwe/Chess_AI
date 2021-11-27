
# performance.py: model the performance of the AI

import game


results = []
for _ in range(20):
    results.append(game.run_game())

print("Results:", results)
