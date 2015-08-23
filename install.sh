#!/bin/sh

# /--/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/--/
# Author: Peter Bugaj.

# /--/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/--/
# Purpose: Installation script for testing Prediction IO as part of a coding
# challenge for PumpUp.

# /--/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/--/
# The following script creates a new Prediction IO APP, inserts test data with "Likes",
# runs a product ranking template with the "Likes" included, and then runs test code
# to ensure results are returned with the correct "Likes" ranking.

# /--/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/----/--/
# Assumes Prediction IO is already installed locally, along with a matching local version
# of Hadoop, Spark, Zookeeper, Python, Java and Scala, and that all PATH names are set
# correctly.



# Set the APP ID to use for testing.
APPNAME="Test"


# Create a new Prediction IO APP.
echo "Creating a new APP with the name" $APPNAME ".\n"
echo "Creating a new APP with the name" $APPNAME ".\n" >> output.log
pio app new $APPNAME > output.log


# Save the new access key.
APPDATA=$(pio app show $APPNAME)
APPKEYNAME="Access Key: "
ACCESSDATA=$(echo ${APPDATA/*$APPKEYNAME/})
ACCESSKEY=$(echo ${ACCESSDATA/" | (all)"/})
echo "Created an access key" $ACCESSKEY ".\n" >> output.log


# Import test data.
echo "Importing test data.\n"
echo "Importing test data.\n" >> output.log
python test/import_testdata.py --access_key $ACCESSKEY >> output.log


# Build the engine.
echo "Building the recommendation engine.\n"
echo "Building the recommendation engine.\n" >> output.log
pio build --verbose >> output.log


# Train the engine.
echo "Training the recommendation engine.\n"
echo "Training the recommendation engine.\n" >> output.log
pio train >> output.log


# Deploy the engine.
echo "Deploying the recommendation engine.\n"
echo "Deploying the recommendation engine.\n" >> output.log
pio deploy </dev/null &>/dev/null &


# Print confirmation message.
echo "Installation complete.\n"
echo "For more verbose information, see output in the output.log file created.\n"
echo "To run test, execute 'python test/tests.py'\n"