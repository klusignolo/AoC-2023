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
        self.inputs = {}
        self.next_pulse_to_send = []
        self.has_pending_outputs = True
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
    

    
    """Processes the input pulse, returning a list of modules that should process next"""
    def receive_pulse(self, source, pulse):
        self.prev_state = self.state
        if self.type == "f":
            self.state = self.state if pulse else not self.state
        elif self.type == "c":
            self.inputs[source] = pulse
            self.state = False
            for v in self.inputs.values():
                if not v:
                    self.state = True
                    break
        if self.type == "f" and pulse:
            self.has_pending_outputs = False # Flip flop that did not change state transmits no outputs
        else:
            self.next_pulse_to_send.append(self.state)
            self.has_pending_outputs = True
        
    
    def send_pulses(self):
        next_pulse = self.next_pulse_to_send.pop(0)
        global HIGH_COUNT
        global LOW_COUNT
        for output in self.outputs:
            if next_pulse:
                HIGH_COUNT += 1
            else:
                LOW_COUNT += 1
            try:
                #state_str = "HIGH" if next_pulse else "LOW"
                #print(f"{self.name} -{state_str}-> {output}")
                MODULES[output].receive_pulse(self.name, next_pulse)
            except KeyError:
                if not next_pulse:
                    raise Exception
                else:
                    continue
        return self.outputs

with open("modules.txt", "r") as file:
    parsed_modules = [Module(line) for line in file.read().splitlines()]
    MODULES = {m.name: m for m in parsed_modules}

# Configure inputs of conjunctions
for source in MODULES.values():
    for destination in source.outputs:
        try:
            if MODULES[destination].type == "c" and source.name not in MODULES[destination].inputs:
                MODULES[destination].inputs[source.name] = False
        except KeyError:
            continue

def press_button():
    global LOW_COUNT
    LOW_COUNT += 1
    MODULES["broadcaster"].receive_pulse("button", False) # Button push
    next_senders = ["broadcaster"]
    while len(next_senders) > 0:
        next_sender = next_senders.pop(0)
        MODULES[next_sender].send_pulses()
        for m in MODULES[next_sender].outputs:
            try:
                if MODULES[m].has_pending_outputs:
                    next_senders.append(m)
            except KeyError:
                continue

try:
    button_count = 0
    while True:
        button_count += 1
        press_button()
except:
    print(f"FOUND IT AFTER {button_count} PRESSES")
# 2718854840 too high
# 700596822 LOW
# 151227080 Low
# 744504136 744504136
print(f"High: {HIGH_COUNT}, Low: {LOW_COUNT}. Product: {HIGH_COUNT * LOW_COUNT}")