from helpers.secret import *
import datetime
import os
import sys

secret_expiration_time_years = 2.5
secret_expiration_time_weeks = 52 * secret_expiration_time_years

def get_secret_expiration():
    secret_archive_expiration = datetime.datetime.now() + datetime.timedelta(weeks=secret_expiration_time_weeks) 
    secret_archive_expiration = secret_archive_expiration.strftime('%s')
    print("Expiration time")
    return secret_archive_expiration

def secret_expiration_check(expiration_time):
    current_time = datetime.datetime.now()
    current_time = current_time.strftime('%s')
    if (current_time > expiration_time):
        return True
    else:
        return False

secretmanager_secret_name = os.environ['zabbix_secret_name']
secretmanager_archive_name = os.environ['zabbix_secret_archive']

hardcoded_secret = sys.argv[1]

production_secret_archive = secret(secretmanager_archive_name)
secret_archive = production_secret_archive.get_secret()
secret_archive = json.loads(secret_archive)

print("Adding manually defined secret to archive")
## Stores the expiration date in epcoh as the key and secret as the value....
secret_archive[get_secret_expiration()] = hardcoded_secret

print("Checking for any expired secrets")
expired_secrets = []
for secret_value in secret_archive:
    if (secret_expiration_check(secret_value)):
        ## Remove Expired Secret
        expired_secrets.append(secret_value)

for secret_value in expired_secrets:
    del secret_archive[secret_value]
if (len(expired_secrets) > 0):
    print("Removed",str(len(expired_secrets)),"expired secrets")
else:
    print("No expired secrets to remove...")

print("Resyncing the secret archive...")
secret_archive = json.dumps(secret_archive)
production_secret_archive.set_secret(secret_archive)