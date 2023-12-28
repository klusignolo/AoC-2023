from copy import deepcopy


with open("test.txt", "r") as file:
    circuit = file.read().splitlines()
connections: dict[str, list[str]] = {}
for line in circuit:
    parse = line.split(": ")
    in_comp = parse[0]
    out_comps = parse[1].split()
    if in_comp in connections.keys():
        connections[in_comp].extend(out_comps)
    else:
        connections[in_comp] = out_comps
    for comp in out_comps:
        if comp in connections.keys():
            connections[comp].append(in_comp)
        else:
            connections[comp] = [in_comp]

conn_counts: dict[str,int] = {key: 0 for key in connections.keys()}
for key, vals in connections.items():
    vals.sort()

group_one = []
group_two = []
cons_for_counting = deepcopy(connections)
while len(group_one) < 3:
    for key, vals in cons_for_counting.items():
        if len(vals) > 0 and vals[0] in conn_counts.keys():
            conn_counts[vals.pop(0)] += 1
    max_one = max(conn_counts, key=conn_counts.get)
    group_one.append(max_one)
    del conn_counts[max_one]
    max_two = max(conn_counts, key=conn_counts.get)
    group_two.append(max_two)
    del conn_counts[max_two]

group_one.sort()
group_two.sort()
team_one = set()
team_two = set()
for i in range(3):
    for key, vals in connections.items():
        if group_one[i] in vals:
            team_one.add(key)
        if group_two[i] in vals:
            team_two.add(key)
conns_to_break = team_one.intersection(team_two)
print(sorted(list(team_one)))
print(sorted(list(team_two)))
print(conns_to_break)