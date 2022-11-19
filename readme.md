# AWS Secrets Manager Credential Rotation
Rotating credentials is an important part of easy to do processes in infosec.. The problem is, you really don't want people to know the new secret.. That's where this comes in.. Run a python script - the current secret, is replaced with a newly generated secret. Following, you run another Python script to cycle the credentials of each service you need to rotate using the new secrets generated in SecretsManager.

There is one small problem though - not all services you need to rotate will be online at any one time... to accomodate servers that are currently offline, unavailable, or otherwise "un-rotate-able", I've added an archive system. This allows us to effectively "cache" secrets for a period of time after rotation. This is a flexible value defined in weeks, however, you could do years, months, hours, minutes, or seconds.. that way, you can cycle passwords as often as you want, and you will still be able to catchup by "remembering" old secrets... bringing previously unavailable services, to compliance. 

This isn't exactly intended to be cloned and ran in your own enviornment, this is a proof of concept.. You can, but some assembly required... namely in the following env vars:

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

Forgive me, this is my first time using the AWS API, so best practices were used to the best of my abilities here..

If you like my work, go check me out on LinkedIn
[https://www.linkedin.com/in/ivanshires](https://www.linkedin.com/in/ivanshires)
