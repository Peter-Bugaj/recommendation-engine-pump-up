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
pio app new $APPNAME > output.log


# Save the new access key.
APPDATA=$(pio app show $APPNAME)

APPKEYNAME="Access Key: "
ACCESSDATA=$(echo ${APPDATA/*$APPKEYNAME/})
ACCESSKEY=$(echo ${ACCESSDATA/" | (all)"/})

echo "Created an access key" $ACCESSKEY ".\n"


# Import test data.
echo "Importing test data.\n"
python test/import_testdata.py --access_key $ACCESSKEY >> output.log


# Build the engine.
echo "Building the recommendation engine.\n"
pio build --verbose >> output.log


# Train the engine.
echo "Training the recommendation engine.\n"
pio train >> output.log


# Deploy the engine.
echo "Deploying the recommendation engine.\n"
pio deploy >> output.log


