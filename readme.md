## Start Uvicorn directly

```bash
uvicorn app:app --host 0.0.0.0
```

First `app` refers to `app.py` (main python file) and the second `app` refers to the FastAPI app inside the main python file.

## Systemd Setup

A systemd service file is created at `/etc/systemd/system/automation-engine-lite.service`

```
[Unit]
Description=Automation Engine Lite

[Service]
User=root
WorkingDirectory=/opt/automation-engine-lite/
ExecStart=/opt/automation-engine-lite/venv/bin/python3 -m uvicorn app:app --host 0.0.0.0

[Install]
WantedBy=multi-user.target
```

Check the status

```bash
systemctl start automation-engine-lite
systemctl status automation-engine-lite
systemctl restart automation-engine-lite
systemctl enable automation-engine-lite
```

## System State

### Ansible

Running version `2.14.9`

```
[root@localhost ~]# ansible --version
ansible [core 2.14.9]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.9.18 (main, Jan  4 2024, 00:00:00) [GCC 11.4.1 20230605 (Red Hat 11.4.1-2)] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True
```

### Python

```
[root@localhost ~]# python --version
Python 3.9.18
```