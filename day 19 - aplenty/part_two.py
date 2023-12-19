from copy import deepcopy
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
    
    def __str__(self):
        return self.condition + ":" + self.destination

    def o_condition(self):
        if self.condition is not None:
            test_param = re.findall(r"(\w+)[<>]", self.condition)[0]
            conditional = re.findall(r"([<>])", self.condition)[0]
            target_val = int(re.findall(r"[<>](\d+)", self.condition)[0])
            if conditional == ">":
                conditional = "<="
            else:
                conditional = ">="
            return f"{test_param}{conditional}{target_val}"
        else:
            return None

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
            
with open("test.txt", "r") as file:
    parsed = file.read().split("\n\n")
    parts = [Part(line) for line in parsed[1].splitlines()]
    workflows ={w.name: w for w in [Workflow(line) for line in parsed[0].splitlines()]}


# Look through all instructions from right to left
# If instruction destination == "A", return Condition.
# If condition is None, condition becomes OPPOSITE of next instruction condition
# At end of instructions, take NAME of workflow and look for workflows that end in that result.
# valid_routes = []
# for name, workflow in workflows.items():
#     for instruction in workflow.instructions:
#         if instruction.destination == "A":
#             valid_routes.append(name)
#             break

# for w_name in valid_routes:
#     workflow = workflows[w_name]
#     conditions = []
#     found_a = False
#     for i in workflow.instructions:
#         if i.destination == "A":
#             found_a = True
#             conditions.append(i.condition)
#         elif not found_a: 
#             continue
#         else:
#             conditions.append(i.o_condition())
#     valid_routes = f
    
# start at IN. look through all possible instruction destinations, gathering conditions that must lead to each destination.
# form new "path" for each fork in the road. A path gets removed IF only destination is R.
p_index = 0
paths: dict[int,list[str]] = {}
final_paths = []
def trace_paths(workflow: Workflow, incoming_path: list[str]):
    outgoing_paths: list[tuple[str, str]] = []
    partial_path = []
    for i in workflow.instructions:
        if i.destination == "R" and i.condition != None:
            partial_path.append(i.o_condition())
        elif i.destination == "A" and i.condition != None:
            final_path = deepcopy(incoming_path)
            if len(partial_path) > 0:
                final_path.extend(partial_path)
            final_path.append(i.condition)
            final_paths.append(final_path)
        elif i.destination == "A":
            final_path = deepcopy(incoming_path)
            if len(partial_path) > 0:
                final_path.extend(partial_path)
            final_paths.append(final_path)
        elif i.destination != "R" and i.condition is not None:
            new_path = deepcopy(incoming_path)
            if len(partial_path) > 0:
                new_path.extend(partial_path)
            new_path.append(i.condition)
            outgoing_paths.append((i.destination, new_path))
            partial_path.append(i.o_condition())
        elif i.destination != "R":
            new_path = deepcopy(incoming_path)
            if len(partial_path) > 0:
                new_path.extend(partial_path)
            outgoing_paths.append((i.destination, new_path))
        elif i.destination == "R":
            continue # dead end
        else:
            print("hh")
    return outgoing_paths

paths_to_search = trace_paths(workflows["in"], incoming_path=[])
while len(paths_to_search) > 0:
    new_paths_to_search = []
    for item in paths_to_search:
        wf_name = item[0]
        p = item[1]
        new_paths_to_search.extend(trace_paths(workflows[wf_name], p))
    paths_to_search = new_paths_to_search

total_options = 0
for valid_path in final_paths:
    max_x = 4000
    min_x = 0
    max_m = 4000
    min_m = 0
    max_a = 4000
    min_a = 0
    max_s = 4000
    min_s = 0
    for condition in valid_path:
        test_param = re.findall(r"(\w+)[<=>]", condition)[0]
        conditional = re.findall(r"\w+(\W+)\d+", condition)[0]
        target_val = int(re.findall(r"[<=>](\d+)", condition)[0])
        match test_param:
            case "x":
                if conditional == ">":
                    min_x = target_val + 1
                elif conditional == ">=":
                    min_x = target_val
                elif conditional == "<":
                    max_x = target_val - 1
                else:
                    max_x = target_val
            case "m":
                if conditional == ">":
                    min_m = target_val + 1
                elif conditional == ">=":
                    min_m = target_val
                elif conditional == "<":
                    max_m = target_val - 1
                else:
                    max_m = target_val
            case "a":
                if conditional == ">":
                    min_a = target_val + 1
                elif conditional == ">=":
                    min_a = target_val
                elif conditional == "<":
                    max_a = target_val - 1
                else:
                    max_a = target_val
            case "s":
                if conditional == ">":
                    min_s = target_val + 1
                elif conditional == ">=":
                    min_s = target_val
                elif conditional == "<":
                    max_s = target_val - 1
                else:
                    max_s = target_val
    x_range = max_x - min_x
    m_range = max_m - min_m
    a_range = max_a - min_a
    s_range = max_s - min_s
    total_options += x_range * m_range * a_range * s_range

#267640439920000
#167409079868000 Test answer
print("Done")
