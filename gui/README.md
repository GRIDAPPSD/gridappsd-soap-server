# User Interface for Common Informatio Model Interoperability Test

## Purpose

This is the User Interface of the application. It starts a webserver which can be accessed in Chrome or Firefox. This server uses the Python SOAP (Simple Object Access Protocol) client Zeep and converts user input to xml messages according to the WSDL (Web Services Description Language) of network services provided by a SOAP server. 

## Requirements

- Python 3
- Virtualenv (optional)
- Running Soap server

## Quick Start


1. Clone this repository (Skip to step 4 if the repository was already cloned and environment was setup)
    ```console
    git clone https://github.com/GRIDAPPSD/gridappsd-soap-server.git
    cd gridappsd-soap-server/    
    ```
    
1. Install the virtual environment (optional)
    ```console
    python -m venv env (optional)
    source env/bin/activate (optional, or source env/Scripts/activate for Windows)
    ```
1. Install the required packages
    ```console
    pip install -r requirements.txt
    ```
1. Start the server
    ```console
    cd gui/dermsapp
    python server.py 
    ```
    
1. Then copy can paste the server address (http://127.0.0.1:8442) into a web browser.
    
