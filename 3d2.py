import json

readme = []

with open("gephi/netchord.csv") as f:
    for line in f:
        data = line.split(",")
        readme.append({"name": data[0], "size": float(data[2].replace("\n", "")), "imports": [data[1]]})
#         nodes.append(str(data[0]))
#         nodes.append(str(data[1]))
#         links.append({"source": "user" + str(data[0]),
#                        "target": "user" + str(data[1]),
#                        "strength": float(data[2])})
# nodes = list(set(nodes))
# nodelist = []

# for n in nodes:
#     nodelist.append({"id": "user" + str(n),
#                      "label": "User " + str(n),
#                      "group": str(n)})

# res = {"nodes": nodelist, "links": links}

# print(readme)
with open('chord2.json', 'w') as outfile:
    json.dump(readme, outfile)

