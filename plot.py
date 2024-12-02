import matplotlib.pyplot as plt

# Data for Nodes Expanded
k_values = [1, 2, 3, 4, 5, 6, 7, 8]
minimax_no_pruning = [8, 57, 400, 2801, 19608, 137256, 960750, 6724200]
minimax_with_pruning = [8, 47, 224, 747, 3456, 11453, 44896, 161528]
expectiminimax = [27, 27, 521, 521, 9907, 9907, 188241, 188241]

# Data for Time Taken
time_minimax_no_pruning = [407.73, 80.94, 315.26, 3.42 * 1000, 8.25 * 1000, 38.84 * 1000, 384.95 * 1000, 29.8 * 60 * 1000]
time_minimax_with_pruning = [623.78, 71.05, 152.77, 0.52592, 1.63 * 1000, 2.77 * 1000, 8.2 * 1000, 36.99 * 1000]
time_expectiminimax = [68.47, 61.83, 240.91, 0.31862, 1.78 * 1000, 2.2 * 1000, 31.75 * 1000, 40.67 * 1000]

# Plot Nodes Expanded
plt.figure(figsize=(12, 6))
plt.plot(k_values, minimax_no_pruning, marker='o', label='Minimax Without α β Pruning')
plt.plot(k_values, minimax_with_pruning, marker='o', label='Minimax With α β Pruning')
plt.plot(k_values, expectiminimax, marker='o', label='ExpectiMiniMax')
plt.xlabel('K')
plt.ylabel('Nodes Expanded')
plt.title('Nodes Expanded by Different Algorithms')
plt.legend()
plt.grid(True)
plt.show()

# Plot Time Taken
plt.figure(figsize=(12, 6))
plt.plot(k_values, time_minimax_no_pruning, marker='o', label='Minimax Without α β Pruning')
plt.plot(k_values, time_minimax_with_pruning, marker='o', label='Minimax With α β Pruning')
plt.plot(k_values, time_expectiminimax, marker='o', label='ExpectiMiniMax')
plt.xlabel('K')
plt.ylabel('Time Taken (ms)')
plt.title('Time Taken by Different Algorithms')
plt.legend()
plt.grid(True)
plt.show()