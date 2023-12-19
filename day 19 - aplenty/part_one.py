import re

class Part:
    def __init__(self, input_str: str):
        self.x = int(re.findall(r"x=(\d+),", input_str)[0])
        self.m = int(re.findall(r"m=(\d+),", input_str)[0])
        self.a = int(re.findall(r"a=(\d+),", input_str)[0])
        self.s = int(re.findall(r"s=(\d+)}", input_str)[0])

class Instruction:
    def __init__(self, input_str: str):
        if ":" in input_str:
            self.destination = re.findall(r":(\w+)", input_str)[0]
            self.condition = re.findall(r"(.+):", input_str)[0]
        else:
            self.destination = input_str
            self.condition = None

    def test_part(self, part: Part) -> bool:
        if not self.condition: return True
        test_param = re.findall(r"(\w+)[<>]", self.condition)[0]
        conditional = re.findall(r"([<>])", self.condition)[0]
        target_val = int(re.findall(r"[<>](\d+)", self.condition)[0])
        match test_param:
            case "x":
                if conditional == ">":
                    return part.x > target_val
                else:
                    return part.x < target_val
            case "m":
                if conditional == ">":
                    return part.m > target_val
                else:
                    return part.m < target_val
            case "a":
                if conditional == ">":
                    return part.a > target_val
                else:
                    return part.a < target_val
            case "s":
                if conditional == ">":
                    return part.s > target_val
                else:
                    return part.s < target_val
        


class Workflow:
    def __init__(self, input_str: str):
        self.name = re.findall(r"(\w+){", input_str)[0]
        self.instructions = [Instruction(line) for line in re.findall(r"{(.+)}", input_str)[0].split(",")]

    def run_part(self, part: Part) -> str:
        for instruction in self.instructions:
            if instruction.test_part(part):
                return instruction.destination
            
with open("input.txt", "r") as file:
    parsed = file.read().split("\n\n")
    parts = [Part(line) for line in parsed[1].splitlines()]
    workflows ={w.name: w for w in [Workflow(line) for line in parsed[0].splitlines()]}

rating_total = 0
for part in parts:
    next_workflow = "in"
    while next_workflow not in ["A", "R"]:
        next_workflow = workflows[next_workflow].run_part(part)
    if next_workflow == "A":
        rating_total += part.x + part.m + part.a + part.s
print(rating_total)
