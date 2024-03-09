#!/bin/bash

value="$1"
echo "Running bash script to change the level to --> $value"
echo "Running Ansible Playbook now..."
ansible-playbook ansible_playbooks/change_config.yml --extra-vars "var1=$value"