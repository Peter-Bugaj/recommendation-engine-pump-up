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