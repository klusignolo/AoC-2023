with open("oasis.txt", "r") as file:
    oasis = [[int(num) for num in line.split()] for line in file.read().splitlines()]

def calculate_history(input: list[int]):
    input.reverse()
    next_input = get_next_input(input)
    ends = [input[0], next_input[0]]
    while next_input[0] != next_input[1]:
        next_input = get_next_input(next_input)
        ends.insert(0,next_input[0])
    histories = [0]
    while len(ends) > 0:
        next_end = ends.pop()
        histories.insert(0, histories[0] + next_end)
    result = histories[0]
    return result



def get_next_input(input: list[int]) -> list[int]:
    next_input = []
    for i in range(len(input) - 1):
        next_input.append(input[i] - input[i+1])
    return next_input

result = 0
for line in oasis:
    result += calculate_history(line)
print(result)