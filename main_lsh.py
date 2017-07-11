import pandas as pd
import logging
from datasketch import MinHash, MinHashLSH
import time
import csv

# This is the similarity threshold
threshold = 0.5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('results/15_lsh_15m.log')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)

start = time.time()
# Load data
print("Loading data...")
data = pd.read_csv("datasets/lsh/15_clusters_15m.csv", quotechar='"')
print("Data loaded! It took %s seconds." % str(time.time() - start))


def get_jaccard_similarity(listA, listB):
    return float(len(set(listA).intersection(set(listB)))) / float(len(set(listA).union(set(listB))))


# Create the signature matrix
sigMat = []

start = time.time()
print("Generate signature matrix...")

for rownum in range(len(data)):
    # The user_id is not the same as the rownum
    user_id = data.iloc[rownum]["USER_ID"]

    # Get the positions for user_id
    positions = set(data.iloc[rownum]["positions"].split(","))

    # Generate the MinHash column for the user's positions
    m = MinHash(num_perm=100)

    for time_space_box in positions:
        m.update(time_space_box.encode('utf8'))

    # Add the signature column of the user into the main signature matrix
    sigMat.append(m)

    # Display the progress of building the signature matrix
    if rownum % 1000 == 0:
        print(rownum, user_id)


print("Signature matrix generated! It took %s seconds." % str(time.time() - start))
print("Applying LSH...")

start = time.time()
# Create the LSH matrix
lsh = MinHashLSH(threshold=threshold, num_perm=100)

for rownum in range(len(sigMat)):
    # For each user generate the lsh signature
    user_id = data.iloc[rownum]["USER_ID"]
    lsh.insert(user_id, sigMat[rownum])

    # Display the progress of building LSH
    if rownum % 1000 == 0:
        print(rownum, user_id)

# Check the first # users
number_of_users_to_check = len(sigMat)

print("LSH applied! It took %s seconds." % str(time.time() - start))
print("Displaying results...")

start = time.time()
# Save the candidates generated by lsh in a csv file, just in case
with open('15_candidates_15m.csv', 'ab') as csvfile:
    candidates_writer = csv.writer(csvfile, delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for rownum in range(number_of_users_to_check):
        # Get the details of the user (user_id, positions)
        user_id = data.iloc[rownum]["USER_ID"]
        positions_query = data.iloc[rownum]["positions"].split(",")

        result = sorted(lsh.query(sigMat[rownum]))
        # print("User %s has the following candidate users (threshold = %s): %s" % (str(user_id), str(threshold), str(result)))
        candidates_writer.writerow([user_id] + result)

        # Bruteforce to validate the generated candidates for the user
        for us_id in result:

            # point_locations contains a list of locations for us_id
            point_locations = data.loc[data["USER_ID"] == us_id]["positions"].iloc[0].split(",")

            sim = get_jaccard_similarity(positions_query, point_locations)
            # Return only the users with sim > threshold and not the same user
            if threshold < sim and user_id != us_id:
                print(user_id, us_id, sim)
                logger.info("%s,%s,%s" % (user_id, us_id, sim))

        # Display the progress of building LSH
        if rownum % 1000 == 0:
            print("Reached row number %s and user id %s" % (rownum, user_id))
print("Results have been generated in %s seconds." % str(time.time() - start))
