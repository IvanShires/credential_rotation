## Credential Rotation via AWS Secrets Manager with a "secrets archive" for any need to circle back to past cycled credentials.
## Archived secrets are in the event that a host is not alive for the initial rotation, and credentials rotated once more... or,
## the original credentials are missed entirely by the rotation software (i.e, in the event credentials are rotated, a server is
## offline, and the software does not save the original credential....)

## By: Ivan Shires

## Purpose: Rotates the current secret, and removes archived secrets older than X number of days
from helpers.secret import *
import datetime
import os

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

secret_production = secret(secretmanager_secret_name) ## secret_name
current_production_secret = secret_production.get_secret()

print("The current secret is",current_production_secret,"- Now Rotating...")
secret_production.rotate_secret()



print("Now adding prior production secret to the secrets archive and checking for expired archive passwords")
production_secret_archive = secret(secretmanager_archive_name)
secret_archive = production_secret_archive.get_secret()
secret_archive = json.loads(secret_archive)



print("Adding current production secret to archive")
## Stores the expiration date in epcoh as the key and secret as the value....
secret_archive[get_secret_expiration()] = current_production_secret

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