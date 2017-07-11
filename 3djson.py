import json

nodes = []
links = []

with open("15_2h.csv") as f:
    for line in f:
        data = line.split(",")
        nodes.append(str(data[0]))
        nodes.append(str(data[1]))
        links.append({"source": "user" + str(data[0]),
                       "target": "user" + str(data[1]),
                       "strength": float(data[2])})
nodes = list(set(nodes))
nodelist = []

for n in nodes:
    nodelist.append({"id": "user" + str(n),
                     "label": "User " + str(n),
                     "group": int(n)})

res = {"nodes": nodelist, "links": links}
with open('rf15.json ', 'w') as outfile:
    json.dump(res, outfile)

