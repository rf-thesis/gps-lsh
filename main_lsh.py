import pandas as pd
import logging
from datasketch import MinHash, MinHashLSH
import time
import csv
import glob
import ntpath
from multiprocessing import Process


# read all data files at once
datafiles = glob.glob("data/*")

# This is the similarity threshold
threshold = 0.5

# print every x rows
rowprinter = 5000

# jaccard similarity calculator
def get_jaccard_similarity(listA, listB):
    return float(len(set(listA).intersection(set(listB)))) / float(len(set(listA).union(set(listB))))


def sig_matrix(data, fname):
    sigMat = []
    for rownum in range(len(data)):
        # The user_id is not the same as the rownum
        user_id = data.iloc[rownum]["device_id"]

        # Get the positions for user_id
        positions = set(data.iloc[rownum]["timespace"].split(","))

        # Generate the MinHash column for the user's positions
        m = MinHash(num_perm=100)

        for time_space_box in positions:
            m.update(time_space_box.encode('utf8'))

        # Add the signature column of the user into the main signature matrix
        sigMat.append(m)

        # Display the progress of building the signature matrix
        if rownum % rowprinter == 0:
            print("%-22s sigmat gen at row: %s" % (fname, rownum))
    return sigMat


def run_lsh(sigMat, data, fname):
    lsh = MinHashLSH(threshold=threshold, num_perm=100)

    for rownum in range(len(sigMat)):
        # For each user generate the lsh signature
        user_id = data.iloc[rownum]["device_id"]
        lsh.insert(user_id, sigMat[rownum])

        # Display the progress of building LSH
        if rownum % rowprinter == 0:
            print("%-22s LSH calc at row: %s" % (fname, rownum))

    return lsh


def finder(datafile):
    print("%s: starting to process" % datafile)
    fname = ntpath.basename(datafile)
    # create logger to write output
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('results/%s' % fname)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # load data
    start = time.time()
    data = pd.read_csv(datafile, quotechar='"', delimiter=";")
    print("%-22s loaded -- %s sec" % (fname, str(time.time() - start)))

    # generate signature matrix
    start = time.time()
    print("%-22s start sigmat" % fname)
    sigMat = sig_matrix(data, fname)
    print("%-22s sigmat done --  %s sec" % (fname, str(time.time() - start)))

    start = time.time()
    print("%-22s start LSH" % fname)
    lsh = run_lsh(sigMat, data, fname)
    print("%-22s LSH done --  %s sec" % (fname, str(time.time() - start)))

    # Check the first # users
    number_of_users_to_check = len(sigMat)

    start = time.time()
    print("%-22s writing results" % fname)

    for rownum in range(number_of_users_to_check):

        # Get the details of the user (user_id, positions)
        user_id = data.iloc[rownum]["device_id"]
        positions_query = data.iloc[rownum]["timespace"].split(",")
        result = sorted(lsh.query(sigMat[rownum]))

        # Bruteforce to validate the generated candidates for the user
        for us_id in result:
            # point_locations contains a list of locations for us_id
            point_locations = data.loc[data["device_id"] == us_id]["timespace"].iloc[0].split(",")

            sim = get_jaccard_similarity(positions_query, point_locations)
            if threshold < sim and user_id != us_id:
                logger.info("%s,%s,%s" % (user_id, us_id, sim))

        # Display the progress of building LSH
        if rownum % rowprinter == 0:
            logger.info("%-22s LSH display at row: %s" % (fname, rownum))

    print("%-22s results done --  %s sec" % (fname, str(time.time() - start)))




# for d in datafiles:
#     finder(d)

starter = time.time()
processlist = []
for d in datafiles:
    p = Process(target=finder, args=(d,))
    processlist.append(p)

for p in processlist:
    p.start()

for p in processlist:
    p.join()

print("Total time: %s" % str(time.time() - starter))







