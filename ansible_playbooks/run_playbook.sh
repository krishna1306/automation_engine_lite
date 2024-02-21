#!/bin/bash

data="$1"
echo "Received data: $data"
echo "Running Ansible Playbook now..."
ansible-playbook ansible_playbooks/test_play.yml -i ansible_playbooks/inventory.ini --extra-vars "var1=value1 var2=value2"