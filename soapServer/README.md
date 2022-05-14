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
5. Start another terminal and clone this repository (Skip to step 7 if the repository was already cloned and environment was setup)
    ```console
    git clone https://github.com/GRIDAPPSD/gridappsd-soap-server.git
    cd gridappsd-soap-server/    
    ```    
6. Install the virtual environment (optional)
    ```console
    python -m venv env (optional)
    source env/bin/activate (optional, or source env/Scripts/activate for Windows)
    ```
7. Install the required packages
    ```console
    pip install -r requirements.txt
    ```
1. Start the server
    ```console
    cd soapServer
    python soap_server.py 
    ```
Now this soap server is running in the background, user can use the [DER GUI](http://127.0.0.1:8442/) and start testing.

    
##