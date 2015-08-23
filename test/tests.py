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


"""
TEST1: Provide no parameters and expect all data to be returned.
"""
def test_RecommendationEngine_NoParameters():
    if len(engine_client.send_query({"" : ""})['likeScores']) == len(test_data):
        print "TEST1 has succeeded!"
        return True
    else:
        TESTS_FAILED +=1
        print "TEST1 has faied!"
        return False


"""
TEST2: Provide a very high limit and expect all data to be returned.
"""
def test_RecommendationEngine_HighLimit():
    if len(engine_client.send_query({"limit" : "100"})['likeScores']) == len(test_data):
        print "TEST2 has succeeded!"
        return True
    else:
        TESTS_FAILED +=1
        print "TEST2 has faied!"
        return False


"""
TEST3: Provide a low limit and expect the given number of elements to be returned.
"""
def test_RecommendationEngine_LowLimit():
    if len(engine_client.send_query({"limit" : "7"})['likeScores']) == 7:
        print "TEST3 has succeeded!"
        return True
    else:
        print "TEST3 has faied!"
        return False


"""
TEST4: Test that the data returned is sorted in descending order.
"""
def test_RecommendationEngine_DescendingOrder():
    elements = engine_client.send_query({"limit" : "100"})['likeScores'];
    unsorted = False;
    for i in range(0, len(elements) - 1):
        if int(elements[i]['likes']) < int(elements[i + 1]['likes']):
            unsorted = True
    if unsorted == False:
        print "TEST4 has succeeded!"
        return True
    else:
        print "TEST4 has faied!"
        return False


"""
TEST5: Test that each post returned has the expected
number of likes as stored in the test data.
"""
def test_RecommendationEngine_CheckLikeCount():
    elements = engine_client.send_query({"limit" : "100"})['likeScores'];
    unmatching = False;
    for actual_element in elements:

        expected_likes = int(test_data[actual_element['postID']])
        actual_likes = int(actual_element['likes'])
        if expected_likes != actual_likes:
            unmatching = True

    if unmatching == False:
        print "TEST5 has succeeded!"
        return True
    else:
        print "TEST5 has faied!"
        return False


"""
TEST6: Test that the three popular posts
created for testing are correct.
"""
def test_RecommendationEngine_PopularPosts():
    elements = engine_client.send_query({"limit" : "100"})['likeScores'];
    if elements[0]['postID'] == 'p100' and elements[1]['postID'] == 'p101' and elements[2]['postID'] == 'p102':
        print "TEST6 has succeeded!"
        return True
    else:
        print "TEST6 has faied!"
        return False


"""
TEST7: Test that the posts returned start from the post with the last post ID specified.
"""
def test_RecommendationEngine_LastPostId():
    elements = engine_client.send_query({"lastPostId" : "p102", "limit" : "100"})['likeScores'];
    if len(elements) == len(test_data) - 2:
        print "TEST7 has succeeded!"
        return True
    else:
        print "TEST7 has faied!"
        return False


"""
TEST8: Test that the posts returned start from the post with the last post
ID specified and are properly limited as specified by the limit parameter.
"""
def test_RecommendationEngine_LastPostIdWithLimit():
    elements = engine_client.send_query({"lastPostId" : "p102", "limit" : "3"})['likeScores'];
    if len(elements) == 3:
        print "TEST8 has succeeded!"
        return True
    else:
        print "TEST8 has faied!"
        return False


"""
TEST9: Test that the posts returned start from the post with the last post
ID specified and that all the remaining posts following are return if no
limit parameter is given.
"""
def test_RecommendationEngine_LastPostIdWithoutLimit():
    elements = engine_client.send_query({"lastPostId" : "p102"})['likeScores'];
    if len(elements) == len(test_data) - 2:
        print "TEST9 has succeeded!"
        return True
    else:
        print "TEST9 has faied!"
        return False


test_RecommendationEngine_NoParameters()
test_RecommendationEngine_HighLimit()
test_RecommendationEngine_LowLimit()
test_RecommendationEngine_DescendingOrder()
test_RecommendationEngine_CheckLikeCount()
test_RecommendationEngine_PopularPosts()
test_RecommendationEngine_LastPostId()
test_RecommendationEngine_LastPostIdWithLimit()
test_RecommendationEngine_LastPostIdWithoutLimit()

print ""
