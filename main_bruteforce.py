import pandas as pd
import logging
import threading

treshold = 0.5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('15.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# load data
print("Loading data")
data = pd.read_csv("datasets/lsh/top100_15.csv", quotechar='"')
print("Data loaded")

def runner(d, m):
    user_m = data.iloc[m]["USER_ID"]
    positions_m = set(data.iloc[m]["positions"].split(","))
    sim = len(positions_d.intersection(positions_m)) / len(positions_d.union(positions_m))
    if sim > treshold:
        logger.info("%s,%s,%s" % (user_d, user_m, sim))
        print("\t - Similar to %s: %s" % (user_m, sim))


for d in range(len(data)):
    user_d = data.iloc[d]["USER_ID"]
    print("Checking user %s" % user_d)
    positions_d = set(data.iloc[d]["positions"].split(","))
    for m in range(d + 1, len(data)):
        threading.Thread(target=runner, name="CALC",
                         args=(d, m)).start()
