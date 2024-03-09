import json
import random
from fastapi import FastAPI, Request
from pydantic import BaseModel, conint, Field
import subprocess
import logging

# logging configuration
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# add http basic auth
from typing import Annotated, List

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

# Define a Pydantic model for changing the config
class ChangeValue(BaseModel):
    value: str

# Define a Pydantic model for Matrix integration
class KpiAlertTracker(BaseModel):
    time: str = Field(..., alias="Time")
    kpi_alert_tracker_id: str = Field(..., alias="Kpi Alert Tracker Id")
    current_state: str = Field(..., alias="Current State")
    previous_state: str = Field(..., alias="Previous State")
    correlation_id: str = Field(..., alias="Correlation Id")
    last_alert: str = Field(..., alias="Last Alert")
    add_time: str = Field(..., alias="Add Time")
    value: str = Field(..., alias="Value")
    uid: str = Field(..., alias="Uid")
    severity: str = Field(..., alias="Severity")
    controller_id: int = Field(..., alias="Controller Id")
    node_id: int = Field(..., alias="Node Id")
    source_data_type: str = Field(..., alias="Source Data Type")
    incident_name: str = Field(..., alias="Incident Name")
    number_of_issues: int = Field(..., alias="Number Of Issues")
    number_of_devices: int = Field(..., alias="Number Of Devices")
    matrix_server: str = Field(..., alias="Matrix Server")


app = FastAPI()

@app.get("/")
def check_status(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"status": "working"}

@app.post("/change_config")
def take_action(change_value: ChangeValue, credentials: Annotated[HTTPBasicCredentials, Depends(security)], request: Request):

    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    previous_level = config_data['link_bw_setting']
    config_data['link_bw_setting'] = change_value.value

    with open('config.json', 'w') as file:
        # Dump the JSON data
        json.dump(config_data, file, indent=4)
    
    logging.info(f"POST request from {request.client.host} - (3) Set Link BW Level : Successfully changed level to --> {change_value.value}")

    return {
        "status" : f"Changed the link BW level from {previous_level} to {change_value.value}"
    }, 200
    

@app.get("/get_link_kpis/{link_id}")
async def get_link_kpis(link_id: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    tx = 0
    rx = 0

    # read the settings from the json config file
    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    if config_data.get('link_bw_setting') == "2":
        tx = random.randint(60, 70)
    elif config_data.get('link_bw_setting') == "1":
        tx = random.randint(50, 60)
    else:
        tx = random.randint(80,100)

    sample_kpi_data = {
        "link_id": link_id,
        "eth1/1": {
            "tx": tx,
            "rx": rx
            },
        }
    return sample_kpi_data

@app.post("/set_link_bw_level/{level}")
def set_link_bw_level(level, kpi_alert_tracker: KpiAlertTracker, credentials: Annotated[HTTPBasicCredentials, Depends(security)], request: Request):
    
    logging.info(f"POST request from {request.client.host} - (1) Set Link BW Level : Received to change to level --> {level}")
    
    if kpi_alert_tracker.current_state != "c":
        logging.error(f"POST request - Set Link BW Level : Invalid current state in payload. Current state should be c. But it is {kpi_alert_tracker.current_state}")
        return {
            "status": f"Current state is {kpi_alert_tracker.current_state}. It should be c"
        }

    set_level = level
    logging.info(f"POST request from {request.client.host} - (2) Set Link BW Level : Internally changed level to --> {level}")

     # Define the path to the shell script
    script_path = "ansible_playbooks/run_playbook.sh"

    # Run the shell script
    result = subprocess.run(["bash", script_path, set_level], stdout=subprocess.PIPE, text=True)

    if(result.returncode != 0):
        return {'status': 'error', 'data': {'returncode': result.returncode, 'output': result.stdout}}
    return {'status': 'success', 'data': {'payload': kpi_alert_tracker.model_dump(), 'output': result.stdout}}

@app.get("/get_link_bw_level/{link_id}")
async def get_link_bw_level(link_id: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    current_level = config_data['link_bw_setting']

    return {
        "status" : f"Current level is {current_level}"
    }