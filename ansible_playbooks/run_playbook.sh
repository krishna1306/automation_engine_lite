#!/bin/bash

value="$1"
log_file="ansible.log"

echo "Running bash script to change the level to --> $value"
echo "Running Ansible Playbook now..."

ansible_output=$(ansible-playbook ansible_playbooks/change_config.yml --extra-vars "var1=$value" 2>&1)

echo "$(date +"[%Y-%m-%d %H:%M:%S]") -- start" >> $log_file
echo "$ansible_output" | while IFS= read -r line; do
    echo "$line"
done >> $log_file
echo "$(date +"[%Y-%m-%d %H:%M:%S]") -- end" >> $log_file