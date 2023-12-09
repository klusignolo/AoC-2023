with open("oasis.txt", "r") as file:
    oasis = [[int(num) for num in line.split()] for line in file.read().splitlines()]

def calculate_history(input: list[int]):
    next_input = get_next_input(input)
    beginnings = [input[0], next_input[0]]
    while sum([abs(i) for i in next_input]) != 0:
        next_input = get_next_input(next_input)
        beginnings.append(next_input[0])
    histories = [0]
    while len(beginnings) > 0:
        next_begin = beginnings.pop()
        histories.insert(0, next_begin - histories[0])
    result = histories[0]
    return result



def get_next_input(input: list[int]) -> list[int]:
    next_input = []
    for i in range(len(input) - 1):
        next_input.append(input[i+1] - input[i])
    return next_input

result = 0
for line in oasis:
    result += calculate_history(line)
print(result)