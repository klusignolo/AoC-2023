from copy import deepcopy

with open("garden.txt", "r") as file:
    garden = [[char for char in line] for line in file.read().splitlines()]
starting_pos = None
for row in range(len(garden)):
    if starting_pos == None:
        for col in range(len(garden[row])):
            if garden[row][col] == "S":
                starting_pos = f"{col},{row}"
                garden[row][col] = "."
                break
    else:
        break
total_steps = 64
even_plots_visited = set([starting_pos]) # Starting position is here because 0 is even
odd_plots_visited = set()
next_even_plots = set()
next_odd_plots = set([starting_pos])
for i in range(1, total_steps+1):
    print(i)
    is_even = i % 2 == 0
    if is_even:
        next_plots = next_even_plots
        next_odd_plots.clear()
    else:
        next_plots = next_odd_plots
        next_even_plots.clear()
    for plot_str in next_plots:
        pos = plot_str.split(",")
        row = int(pos[1])
        col = int(pos[0])
        up = (col, row - 1) if row > 0 else None
        right = (col + 1, row) if col < len(garden[row]) - 1 else None
        down = (col, row + 1) if row < len(garden) - 1 else None
        left = (col - 1, row) if col > 0 else None
        if up:
            plot_str = f"{up[0]},{up[1]}"
            if is_even and plot_str not in even_plots_visited and garden[up[1]][up[0]] == ".":
                next_odd_plots.add(plot_str)
            elif not is_even and plot_str not in odd_plots_visited and garden[up[1]][up[0]] == ".":
                next_even_plots.add(plot_str)
        if right:
            plot_str = f"{right[0]},{right[1]}"
            if is_even and plot_str not in even_plots_visited and garden[right[1]][right[0]] == ".":
                next_odd_plots.add(plot_str)
            elif not is_even and plot_str not in odd_plots_visited and garden[right[1]][right[0]] == ".":
                next_even_plots.add(plot_str)
        if down:
            plot_str = f"{down[0]},{down[1]}"
            if is_even and plot_str not in even_plots_visited and garden[down[1]][down[0]] == ".":
                next_odd_plots.add(plot_str)
            elif not is_even and plot_str not in odd_plots_visited and garden[down[1]][down[0]] == ".":
                next_even_plots.add(plot_str)
        if left:
            plot_str = f"{left[0]},{left[1]}"
            if is_even and plot_str not in even_plots_visited and garden[left[1]][left[0]] == ".":
                next_odd_plots.add(plot_str)
            elif not is_even and plot_str not in odd_plots_visited and garden[left[1]][left[0]] == ".":
                next_even_plots.add(plot_str)
    if is_even:
        even_plots_visited.update(next_odd_plots)
    else:
        odd_plots_visited.update(next_even_plots)

answer = len(even_plots_visited)
print(answer)
