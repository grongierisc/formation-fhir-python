#!/bin/bash
# This script is used to initialize the InterSystems IRIS database with the necessary configuration files and data.

# First, merge the main configuration file
if [ ! -f /irisdev/app/initdb.d/merge.cpf ]; then
    echo "Configuration file /irisdev/app/initdb.d/merge.cpf not found."
    exit 1
fi
echo "Merging configuration file /irisdev/app/initdb.d/merge.cpf into IRIS database..."
iris merge iris /irisdev/app/initdb.d/merge.cpf
if [ $? -ne 0 ]; then
    echo "Error during merge of /irisdev/app/initdb.d/merge.cpf"
    exit 1
fi

# Init also the iris fhir python strategy settings if the file exists
python3 -m iris_fhir_python_strategy --namespace FHIRSERVER

# Now, run the initialization script
if [ -f /irisdev/app/initdb.d/iris.script ]; then
    echo "Running initialization script /irisdev/app/initdb.d/iris.script..."
    iris session iris < /irisdev/app/initdb.d/iris.script
    if [ $? -ne 0 ]; then
        echo "Error during initialization script /irisdev/app/initdb.d/iris.script"
        exit 1
    fi
fi

# Check if iop command is available and run it if it is
if command -v iop &> /dev/null; then
    echo "Running iop command to import additional configuration..."
    iop --init --namespace EAI
    iop --migrate /irisdev/app/src/EAI/python/EAI/settings.py
