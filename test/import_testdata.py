import argparse
from collections import Counter
import os
import predictionio
import random

SEED = 7

"""
Import test data for the recommendation engine.
"""
def import_events(client):
  random.seed(SEED)
  print client.get_status()
  print "Importing test data..."

  # Generate 20 users, with user ids u1,u2,....,u10.
  user_ids = ["u%s" % i for i in range(1, 21)]
  for user_id in user_ids:
    client.create_event(
      event="$set",
      entity_type="user",
      entity_id=user_id
    )

  # Generate 50 posts, with post ids p1,p2,....,p50.
  post_ids = ["p%s" % p for p in range(1, 51)]
  for post_id in post_ids:
    client.create_event(
      event="$set",
      entity_type="post",
      entity_id=post_id
    )

  # Select 10 random users to randomly like 20 posts.
  likes_per_post = Counter()
  for user_id in random.sample(user_ids, 10):
    for liked_post in random.sample(post_ids, 20):
      client.create_event(
        event="like",
        entity_type="user",
        entity_id=user_id,
        target_entity_type="post",
        target_entity_id=liked_post
      )
      likes_per_post[liked_post] += 1;

  # Create three popular posts for more specific testing
  # purposes. These posts will have up to 17 to 20 likes.
  for i in range(0, 3):
    popular_id = "p" + str(100 + i)
    client.create_event(
      event="$set",
      entity_type="post",
      entity_id=popular_id
    )
    for user_id in random.sample(user_ids, 20 - i):
      client.create_event(
        event="like",
        entity_type="user",
        entity_id=user_id,
        target_entity_type="post",
        target_entity_id=popular_id
      )
      likes_per_post[popular_id] += 1;

  print "All test data has been imported.\n"

  # Save the test data as expected output to use for testing
  # against actual output when calling the REST APIs.
  testOutputFile = open(
    os.path.dirname(
      os.path.realpath(__file__)) + "/test_data", "w")
  for key in likes_per_post:
    testOutputFile.write(key + " " + str(likes_per_post[key]) + "\n")
  testOutputFile.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="Import test data for recommendation engine")
  parser.add_argument('--access_key', default='invald_access_key')
  parser.add_argument('--url', default="http://localhost:7070")

  args = parser.parse_args()
  print args

  client = predictionio.EventClient(
    access_key=args.access_key,
    url=args.url,
    threads=5,
    qsize=500)
  import_events(client)
