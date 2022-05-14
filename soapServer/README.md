# SOAP Common Informatio Model Interoperability Test

## Purpose

Scripts in this directory set up a SOAP (Simple Object Access Protocol) server that provides network services, which can be used to manage DER in the GridApps-D simulation. Spyne is used to provide the remote procedure call api and generate WSDL that describe all the services available.

## Requirements

1. Python 3
2. [GridApps-D](https://gridappsd.readthedocs.io/en/master/installing_gridappsd/index.html)
3. Virtualenv (optional)

## Quick Start



1. Clone the gridappsd-docker repository
    ```console
    mkdir src // if src exists, change directory to src
    git clone https://github.com/GRIDAPPSD/gridappsd-docker
    cd gridappsd-docker
    ```
2. Run the docker containers
    ```console
    ./run.sh
    ```
3. Once inside the container start gridappsd so Gridapps-d is running in the background.
    ```console
    ./run-gridappsd.sh
    ```
4. Start another terminal and clone this repository (Skip to step 7 if the repository was already cloned and environment was setup)
    ```console
    // go back to the src directory first
    git clone https://github.com/GRIDAPPSD/gridappsd-soap-server.git
    cd gridappsd-soap-server/    
    ```    
5. Install the virtual environment (optional)
    ```console
    python -m venv env (optional)
    source env/bin/activate (optional, or source env/Scripts/activate for Windows)
    ```
6. Install the required packages
    ```console
    pip install -r requirements.txt
    ```
   
7. Set up the power flow model
    ```console
    cd circuit
    python upload_circuit.py
    ```
   
8. Insert enddevices to the model
    ```console
    // go back to the src directory first
    git clone https://github.com/GRIDAPPSD/Powergrid-Models.git -b enddevice
    cd Powergrid-Models/enddevices
    python addUsagePointsandEndDevices.py
    ```
   If user wants to preserve the UUID of the added enddevice, the xml endDevicesAndUsagePoints.xml can be read in instead of generate new UUID in the script by comment/uncomment some of the code. If the script is run as it is, a new endDevicesAndUsagePoints.xml will be generated and can be used later to keep the UUID the same.



10. Start the server
     ```console
     // go back to the src directory first
     cd gridappsd-soap-server/soapServer
     python soap_server.py 
     ```
Now this soap server is running in the background, user can use the [DER GUI](http://127.0.0.1:8442/) and start testing.

    
##