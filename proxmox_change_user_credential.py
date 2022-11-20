## Rotate Proxmox user credentials... This is meant to be a proof of concept

from proxmoxer import ProxmoxAPI
from helpers.secret import *
import os


proxmox_host = os.environ['proxmox_host']
proxmox_user = os.environ['proxmox_user']

secretmanager_secret_name = os.environ['secret_name']
secretmanager_archive_name = os.environ['secret_archive']
default_proxmox_password = os.environ['secret_proxmox_default']

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
    try:
        secret_value = secrets_list.pop()
        print("Trying with credential...")
        proxmox = ProxmoxAPI(
            proxmox_host, user=proxmox_user, password=secret_value, verify_ssl=False
        )
        login_loop = False
    except Exception as e:
        if ("Couldn't authenticate user" in str(e)):
            pass
        else:
            print(e)

print("Changing secret...")
proxmox.access(["password"]).set(userid=proxmox_user,password=current_production_secret)
print("Verifying rotation successful")
try:
    proxmox = ProxmoxAPI(
        proxmox_host, user=proxmox_user, password=current_production_secret, verify_ssl=False
    )
    login_loop = False
except Exception as e:
    if ("Couldn't authenticate user" in str(e)):
        os.exit()
    else:
        print(e)
print("Credential successfully rotated..")