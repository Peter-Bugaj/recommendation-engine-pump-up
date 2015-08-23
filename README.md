# Coding challenge for Pump Up

### Author
Peter Bugaj

### Documentation

This code has been modified from the product ranking template.
For similar documentation please refer to:

http://docs.prediction.io/templates/productranking/quickstart/


### Preprequisite

Prediction IO is already installed locally, along with a
matching local version of Hadoop, Spark, Zookeeper, Python,
Java and Scala, and that all PATH names are set.

### Installion

##### Step 1:
Launch prediction io locally by running the command:
  pio-start-all and pio status

##### Step 2:
Delete the test account used by the engine by running the command:  
  pio app delete Test and pio app new Test

##### Step 3:
Go  to the 'recommendation-engine' directory.
  cd /path_to_folder/recommendation-engine

##### Step 4:
Ensure that the engine.json data has the app name set to "Test".
This is important because the test data created will use this
app name while the installation script is run.

##### Step 5:
Run the install script by running the following command:
  ./install.sh

##### Notes:
install.sh will import test data. This test data is found in
the recommendation-engine/test folder. To run tests on this
data, execute the commmand:

  python test/tests.py

### Tests
Tests are located in the recommendation/test folder.
To run the tests execute the command:

  python test/tests.py
  
The tests will read the test_data file created during installation
and test against it that all data is being returned correctly from
the recommendation engine.

### Usage
##### Return all data with posts in descending order:
curl -H "Content-Type: application/json" \
-d '{}' \
http://localhost:8000/queries.json

##### Return data with posts in descending order with limit specified:
curl -H "Content-Type: application/json" \
-d '{"limit":6}' \
http://localhost:8000/queries.json

##### Return all data with posts starting with the post labelled with the last post ID:
curl -H "Content-Type: application/json" \
-d '{"lastPostId": "p102"}' \
http://localhost:8000/queries.json

##### Return all data with posts starting with the last post ID, and with limit specified:
curl -H "Content-Type: application/json" \
-d '{"lastPostId": "p102", "limit":6}' \
http://localhost:8000/queries.json

##### Note:
The $ACCESS_KEY used below is the key created for the app associated with
prediction io when running the command: pio app new [NEW_APP_NAME]

##### Add a new user with ID 'u123':
curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "$set",
  "entityType" : "user"
  "entityId" : "u123",
  "eventTime" : "2020-11-02T09:39:45.618-08:00"
}'

##### Add a new post with ID 'p123':
curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "$set",
  "entityType" : "post"
  "entityId" : "p123",
  "eventTime" : "2020-11-02T09:39:45.618-08:00"
}'

##### Add a new like event for a post where user 'u123' like post 'p123':
curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "like",
  "entityType" : "user"
  "entityId" : "u123",
  "targetEntityType" : "post",
  "targetEntityId" : "p123",
  "eventTime" : "2014-11-10T12:34:56.123-08:00"
}'