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

##### Step 1.
Launch prediction io locally by running the command:
  pio-start-all and pio status

##### Step 2:
Delete the test account used by the engine by running the command:  
  pio app delete Test and pio app new Test

##### Step 3:
Go  to the 'recommendation-engine' directory.
  cd /path_to_folder/recommendation-engine

##### Step 4.
Ensure that the engine.json data has the app name set to "Test".
This is important because the test data created will use this
app name while the installation script is run.

##### Step 5.
Run the install script by running the following command:
  ./install.sh

##### Notes:

install.sh will import test data, launch the engine, and run a few test
cases to ensure the data was imported correctly and is being returned
successly by the recommendation engine.

### Tests
Tests are located in the recommendation/test folder.
To run the tests execute the command:

  python test/tests.py
  
The tests will read the test_data file created during installation
and test against it that all data is being returned correctly from
the recommendation engine.
