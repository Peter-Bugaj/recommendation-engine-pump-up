import json
import os
import predictionio


"""
File for running test cases to make ensure
the recommendation engine is working correctly.
"""

# The client to test against.
engine_client = predictionio.EngineClient(url="http://localhost:8000")

# Load the test data to compare against.
test_data = {}
file_name = os.path.dirname(os.path.realpath(__file__)) + "/test_data"
with open(file_name, "r") as reader:
    for line in reader:
        temp = line.strip().split(" ")
        if len(temp) == 2:
            test_data[temp[0]] = int(temp[1])


TESTS_FAILED = 0
TESTS_SUCCEEDED = 0


"""
TEST1: Provide no parameters and expect all data to be returned.
"""
if len(engine_client.send_query({"" : ""})['likeScores']) == len(test_data):
    TESTS_SUCCEEDED += 1
    print "TEST1 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST1 has faied!"


"""
TEST2: Provide a very high limit and expect all data to be returned.
"""
if len(engine_client.send_query({"limit" : "100"})['likeScores']) == len(test_data):
    TESTS_SUCCEEDED += 1
    print "TEST2 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST2 has faied!"
    

"""
TEST3: Provide a low limit and expect the given number of elements to be returned.
"""
if len(engine_client.send_query({"limit" : "7"})['likeScores']) == 7:
    TESTS_SUCCEEDED += 1
    print "TEST3 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST3 has faied!"
    

"""
TEST4: Test that the data returned is sorted in descending order.
"""
elements = engine_client.send_query({"limit" : "100"})['likeScores'];
unsorted = False;
for i in range(0, len(elements) - 1):
    if int(elements[i]['likes']) < int(elements[i + 1]['likes']):
        unsorted = True
if unsorted == False:
    TESTS_SUCCEEDED += 1
    print "TEST4 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST4 has faied!"


"""
TEST5: Test that each post returned has the expected
number of likes as stored in the test data.
"""
elements = engine_client.send_query({"limit" : "100"})['likeScores'];
unmatching = False;
for actual_element in elements:

    expected_likes = int(test_data[actual_element['postID']])
    actual_likes = int(actual_element['likes'])
    if expected_likes != actual_likes:
        unmatching = True
        
if unmatching == False:
    TESTS_SUCCEEDED += 1
    print "TEST5 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST5 has faied!"


"""
TEST6: Test that the three popular posts
created for testing are correct.
"""
elements = engine_client.send_query({"limit" : "100"})['likeScores'];
if elements[0]['postID'] == 'p100' and elements[1]['postID'] == 'p101' and elements[2]['postID'] == 'p102':
    TESTS_SUCCEEDED += 1
    print "TEST6 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST6 has faied!"


"""
TEST7: Test that the posts returned start from the post with the last post ID specified.
"""
elements = engine_client.send_query({"lastPostId" : "p102", "limit" : "100"})['likeScores'];
if len(elements) == len(test_data) - 2:
    TESTS_SUCCEEDED += 1
    print "TEST7 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST7 has faied!"


"""
TEST8: Test that the posts returned start from the post with the last post
ID specified and are properly limited as specified by the limit parameter.
"""
elements = engine_client.send_query({"lastPostId" : "p102", "limit" : "3"})['likeScores'];
if len(elements) == 3:
    TESTS_SUCCEEDED += 1
    print "TEST8 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST8 has faied!"


"""
TEST9: Test that the posts returned start from the post with the last post
ID specified and that all the remaining posts following are return if no
limit parameter is given.
"""
elements = engine_client.send_query({"lastPostId" : "p102"})['likeScores'];
if len(elements) == len(test_data) - 2:
    TESTS_SUCCEEDED += 1
    print "TEST9 has succeeded!"
else:
    TESTS_FAILED +=1
    print "TEST9 has faied!"
