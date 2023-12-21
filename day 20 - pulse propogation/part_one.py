# Conjunction: & - Remembers most recent pulse from ALL inputs. Transmits LOW if all are high. Transmits HIGH if any are low.
# Flip-flip % - Toggles state when if it receives a LOW input, then transmits its current state.
# Broadcaster - Forwards input pulse to all of its outputs
MODULES: dict[str, "Module"] = {}
HIGH_COUNT = 0
LOW_COUNT = 0
class Module:
    type: str
    outputs: list[str]
    state: bool
    prev_state: bool

    def __repr__(self):
        state = "HIGH" if self.state else "LOW"
        return f"{self.name}: {state}"

    def __init__(self, unparsed_str: str):
        parse1 = unparsed_str.split(" -> ")
        self.inputs = []
        self.pending_inputs = []
        self.pending_outputs = []
        if parse1[0].startswith("&"):
            self.type = "c"
            self.name = parse1[0][1:]
        elif parse1[0].startswith("%"):
            self.type = "f"
            self.name = parse1[0][1:]
        else:
            self.type = "b"
            self.name = parse1[0]

        self.state = False
        self.prev_state = False
        self.outputs = parse1[1].split(", ")
    
    def receive_pending_input(self, source: str, input: bool):
        print(f"adding input {source, input} to {self.name}")
        self.pending_inputs.append((source, input))
    
    """Processes the input pulse, returning a list of modules that should process next"""
    def process_input(self):
        self.prev_state = self.state
        pi = self.pending_inputs.pop(0)
        source = pi[0]
        input = pi[1]
        print(f"removing input {source, input} from {self.name}")
        global HIGH_COUNT
        global LOW_COUNT
        if input:
            HIGH_COUNT += 1
        else:
            LOW_COUNT += 1
        state_str = "HIGH" if input else "LOW"
        print(f"{source} -{state_str}-> {self.name}")
        if self.type == "f":
            self.state = self.state if input else not self.state
        elif self.type == "c":
            self.state = False
            for v in self.inputs:
                if not MODULES[v].state:
                    self.state = True
                    break
        if self.type == "f" and input:
            self.pending_outputs = [] # Flip flop that did not change state transmits no outputs
        else:
            self.pending_outputs = self.outputs
        return self.pending_outputs
        
    
    def send_pulses(self):
        if self.type == "c":
            self.state = False
            for v in self.inputs:
                if not MODULES[v].state:
                    self.state = True
                    break
        for output in self.outputs:
            try:
                MODULES[output].receive_pending_input(self.name, self.state)
            except KeyError:
                continue
        return self.outputs

with open("test.txt", "r") as file:
    parsed_modules = [Module(line) for line in file.read().splitlines()]
    MODULES = {m.name: m for m in parsed_modules}
MODULES["output"] = Module("output -> ")
MODULES["output"].outputs = []
# Configure inputs of conjunctions
for m in MODULES.values():
    for output in m.outputs:
        try:
            if MODULES[output].type == "c" and m.name not in MODULES[output].inputs:
                MODULES[output].inputs.append(m.name)
        except KeyError:
            continue

def press_button():
    MODULES["broadcaster"].receive_pending_input("button", False) # Button push
    MODULES["broadcaster"].process_input()

    next_modules = ["broadcaster"]
    while len(next_modules) > 0:
        module_to_process = next_modules.pop(0)
        transmitted_outputs = MODULES[module_to_process].send_pulses()
        for m in transmitted_outputs:
            MODULES[m].process_input()
            next_modules.extend(MODULES[m].pending_outputs)


for i in range(1):
    press_button()
# 2718854840 too high
# 2718892737
print(f"High: {HIGH_COUNT}, Low: {LOW_COUNT}. Product: {HIGH_COUNT * LOW_COUNT}")