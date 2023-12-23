with open("test.txt", "r") as file:
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
y = 1
x = 0
width = len(garden[0])
height = len(garden)
total_steps = 30
even_plots_visited = set([starting_pos]) # Starting position is here because 0 is even
odd_plots_visited = set()
next_even_plots = set()
next_odd_plots = set([starting_pos])
previous_possible_paths = 1
for i in range(1, total_steps+1):
    is_even = i % 2 == 0
    if is_even:
        next_plots = next_even_plots
        next_odd_plots.clear()
    else:
        next_plots = next_odd_plots
        next_even_plots.clear()
    for plot_str in next_plots:
        pos = plot_str.split(",")
        row = int(pos[y])
        col = int(pos[x])
        up = [col, row - 1]
        right = [col + 1, row]
        down = [col, row + 1]
        left = [col - 1, row]
        up_plot_str = f"{up[x]},{up[y]}"
        right_plot_str = f"{right[x]},{right[y]}"
        down_plot_str = f"{down[x]},{down[y]}"
        left_plot_str = f"{left[x]},{left[y]}"

        if up[y] < 0:
            up[y] = abs(height + up[y]) % height
        elif up[y] >= height:
            up[y] = (up[y] % height)
        if up[x] < 0:
            up[x] = abs(width + up[x]) % width
        elif up[x] >= width:
            up[x] = (up[x] % width)
            
        if down[y] < 0:
            down[y] = abs(height + down[y]) % height
        elif down[y] >= height:
            down[y] = (down[y] % height)
        if down[x] < 0:
            down[x] = abs(width + down[x]) % width
        elif down[x] >= width:
            down[x] = (down[x] % width)

        if left[y] < 0:
            left[y] = abs(height + left[y]) % height
        elif left[y] >= height:
            left[y] = (left[y] % height)
        if left[x] < 0:
            left[x] = abs(width + left[x]) % width
        elif left[x] >= width:
            left[x] = (left[x] % width)

        if right[y] < 0:
            right[y] = abs(height + right[y]) % height
        elif right[y] >= height:
            right[y] = (right[y] % height)
        if right[x] < 0:
            right[x] = abs(width + right[x]) % width
        elif right[x] >= width:
            right[x] = (right[x] % width)

        if up:
            if is_even and up_plot_str not in even_plots_visited and garden[up[y]][up[x]] == ".":
                next_odd_plots.add(up_plot_str)
            elif not is_even and up_plot_str not in odd_plots_visited and garden[up[y]][up[x]] == ".":
                next_even_plots.add(up_plot_str)
        if right:
            if is_even and right_plot_str not in even_plots_visited and garden[right[y]][right[x]] == ".":
                next_odd_plots.add(right_plot_str)
            elif not is_even and right_plot_str not in odd_plots_visited and garden[right[y]][right[x]] == ".":
                next_even_plots.add(right_plot_str)
        if down:
            if is_even and down_plot_str not in even_plots_visited and garden[down[y]][down[x]] == ".":
                next_odd_plots.add(down_plot_str)
            elif not is_even and down_plot_str not in odd_plots_visited and garden[down[y]][down[x]] == ".":
                next_even_plots.add(down_plot_str)
        if left:
            if is_even and left_plot_str not in even_plots_visited and garden[left[y]][left[x]] == ".":
                next_odd_plots.add(left_plot_str)
            elif not is_even and left_plot_str not in odd_plots_visited and garden[left[y]][left[x]] == ".":
                next_even_plots.add(left_plot_str)
    if is_even:
        even_plots_visited.update(next_odd_plots)
    else:
        odd_plots_visited.update(next_even_plots)

answer = len(even_plots_visited)
print(answer)
