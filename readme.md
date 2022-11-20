# AWS Secrets Manager Credential Rotation
Rotating credentials is an important part of easy to do processes in infosec.. The problem is, you really don't want people to know the new secret.. That's where this comes in.. Run a python script - the current secret, is replaced with a newly generated secret. Following, you run another Python script to cycle the credentials of each service you need to rotate using the new secrets generated in SecretsManager.

There is one small problem though - not all services you need to rotate will be online at any one time... to accomodate servers that are currently offline, unavailable, or otherwise "un-rotate-able", I've added an archive system. This allows us to effectively "cache" secrets for a period of time after rotation. This is a flexible value defined in weeks, however, you could do years, months, hours, minutes, or seconds.. that way, you can cycle passwords as often as you want, and you will still be able to catchup by "remembering" old secrets... bringing previously unavailable services, to compliance, even if they miss *multiple* secret rotations.. This avoids having to reset services to "factory", just to bring them up to compliance with the current secrets. 

This isn't exactly intended to be cloned and ran in your own enviornment, this is a proof of concept.. You can, but some assembly required... namely in the following env vars:

## Features
- Allows servers that miss a credential cycle, to be reprovisioned by the credential shuffle tool, to the new secret.
- Allows you to add a archived secret on-demand, in the event a server has a secret in-use that is not known to the software.
- Reduces the risk of malpractice with credentials, as end users *shouldn't* have access to secrets. Only applications.

## Random Bits
Adding a password on an ad-hoc basis (meaning, non-generated password)

    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ python3 zabbix_create_archive_secret.py potato626
    Getting the secret detail for zabbix_secret_archive
    Adding manually defined secret to archive
    Expiration time
    Checking for any expired secrets
    No expired secrets to remove...
    Resyncing the secret archive...
    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ 

This way, it's automatically added into the Secret Manager Archive, so as the software comes across the secret, it will be able to reprovision it to be the new secret.

Creating a new secret for a service (current password output probably should be removed for production)

    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ python3 zabbix_rotate_secret.py 
    Getting the secret detail for zabbix_secret
    The current secret is A8dZWqTXNL6e6UoCpZXjzrxvntVziD - Now Rotating...
    Now adding prior production secret to the secrets archive and checking for expired archive passwords
    Getting the secret detail for zabbix_secret_archive
    Adding current production secret to archive
    Expiration time
    Checking for any expired secrets
    No expired secrets to remove...
    Resyncing the secret archive...
    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ 

Changing User Credential on a Service (in this case, Proxmox)

    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ python3 proxmox_change_user_credential.py 
    Getting the secret detail for lab_password
    Getting the secret detail for lab_password_archive
    Trying with credential...
    Changing secret...
    Verifying rotation successful
    Credential successfully rotated..
    ivans-Mac-mini:aws-secrets-mgr-learning ivan$ 

## How-To

#### ~/.aws/credentials file:

    ivans-Mac-mini:~ ivan$ cat ~/.aws/credentials 
    [default]
    aws_access_key_id={{ redacted }}
    aws_secret_access_key={{} redacted }}
    ivans-Mac-mini:~ ivan$ 

#### ~/.bashrc file:

    ivans-Mac-mini:~ ivan$ cat ~/.bashrc | grep secret
    export secret_archive={{ redacted }}
    export secret_name={{ redacted }}
    export secret_proxmox_default=root
    ivans-Mac-mini:~ ivan$ 

## Misc

Forgive me, this is my first time using the AWS API, so best practices were used to the best of my abilities here..

If you like my work, go check me out on LinkedIn
[https://www.linkedin.com/in/ivanshires](https://www.linkedin.com/in/ivanshires)
