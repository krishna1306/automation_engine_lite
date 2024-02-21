import json
import random
from fastapi import FastAPI
from pydantic import BaseModel, conint
import subprocess
import os

# Define a Pydantic model for the request body
class Payload(BaseModel):
    node_ip: str
    alert_level: str
    action: str = None

class Level(BaseModel):
    value: conint(ge=1, le=3) # type: ignore

app = FastAPI()

@app.get("/")
def check_status():
    return {"status": "working"}

@app.post("/automate")
async def take_action(payload: Payload):

    # Define the path to the shell script
    script_path = "ansible_playbooks/run_playbook.sh"

    # Run the shell script
    result = subprocess.run(["bash", script_path, payload.node_ip], stdout=subprocess.PIPE, text=True)

    if(result.returncode != 0):
        return {'status': 'error', 'data': {'returncode': result.returncode, 'output': result.stdout}}
    return {'status': 'success', 'data': {'payload': payload.model_dump(), 'output': result.stdout}}

@app.get("/get_link_kpis/{link_id}")
async def get_link_kpis(link_id: str):

    tx = 0
    rx = 0

    # read the settings from the json config file
    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    if config_data.get('link_bw_setting') == 2:
        tx = random.randint(60, 70)
    elif config_data.get('link_bw_setting') == 1:
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

@app.post("/set_link_bw_level")
async def set_link_bw_level(level: Level):

    set_level = level.value

    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    previous_level = config_data['link_bw_setting']

    config_data['link_bw_setting'] = set_level

    with open('config.json', 'w') as file:
        # Load the JSON data
        json.dump(config_data, file, indent=4)
    return {
        "status" : f"Changed the link BW level from {previous_level} to {set_level}"
    }

@app.get("/get_link_bw_level/{link_id}")
async def get_link_bw_level(link_id: str):

    with open('config.json', 'r') as file:
        # Load the JSON data
        config_data = json.load(file)

    current_level = config_data['link_bw_setting']

    return {
        "status" : f"Current level is {current_level}"
    }