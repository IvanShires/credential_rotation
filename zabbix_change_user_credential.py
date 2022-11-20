## Rotate Zabbix user credentials... This is meant to be a proof of concept

## FOR THIS TO WORK: YOU NEED TO INCREASE ZABBIX LOGIN ATTEMPTS FROM 5 TO 32

from proxmoxer import ProxmoxAPI
from helpers.secret import *
from pyzabbix import ZabbixAPI,ZabbixAPIException
import os
import time

secretmanager_secret_name = os.environ['zabbix_secret_name']
secretmanager_archive_name = os.environ['zabbix_secret_archive']
default_proxmox_password = os.environ['secret_proxmox_default']

zabbix_url = "http://10.0.0.35/zabbix"
zabbix_user = "Admin"

login_loop = True

## Function that grab's current secrets
secret_production = secret(secretmanager_secret_name) ## secret_name
current_production_secret = secret_production.get_secret()

## Fuction that grabs old secrets
production_secret_archive = secret(secretmanager_archive_name)
secret_archive = production_secret_archive.get_secret()
secret_archive = json.loads(secret_archive)

secrets_list = []
for secret_value in secret_archive:
    secrets_list.append(secret_archive[secret_value])

secrets_list.append(default_proxmox_password)
secrets_list.append(current_production_secret)

while login_loop:
    secret_value = str(secrets_list.pop())
    print("Trying with credential:",secret_value)
    try:
        with ZabbixAPI(url=zabbix_url, user=zabbix_user, password=secret_value) as zapi:
            # Get all monitored hosts
            users = zapi.user.get()
            for user in users:
                if (user['username'] == zabbix_user):
                    user_id = user['userid']
            login_loop = False
    except Exception as e:
        if ("Couldn't authenticate user" in str(e)):
            pass
        else:
            print(e)

print("Changing secret...")

try:
    with ZabbixAPI(url=zabbix_url, user=zabbix_user, password=secret_value) as zapi:
        # Get all monitored hosts
        users = zapi.user.update(
            {
                'userid':user_id,
                'passwd':secret_value,
            }
        )
        print(users)
except Exception as e:
    print(e)

print("Verifying rotation successful")
try:
    with ZabbixAPI(url=zabbix_url, user=zabbix_user, password=secret_value) as zapi:
        # Get all monitored hosts
        users = zapi.user.update(
            {
                'userid':user_id,
                'passwd':current_production_secret,
            }
        )
        print(users)
except Exception as e:
    print("Secret Failed to validate")
print("Credential successfully rotated..")