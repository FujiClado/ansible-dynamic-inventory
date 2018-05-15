### Python Script to Generate Dynamic Inventory Of AWS Ec2-instances.

This Python script will generate  inventory for ansible based on Ec2 tags.

### Script Requirements

- python3
- boto3
- Latest Version of ansible

### HowTo Run This Script.

- Configure awscli with user credentials.
- While Creating ec2 instance add a Tag with Key called "Ansible"
and  colon separated values as group name.

Eg: Key=Ansible  Value=centos:webserver

The above tag will put that instance under two groups, centos and  webserver

- Accessing Dynamic Groups From ansible.

```
[management-node]$ ansible -i inventory.py  centos -m ping
[management-node]$ ansible -i inventory.py  webserver -m ping
```

### Customisation  Options

This section will cover all the variable and their usage
in the script.

---------------------------------------------------

- REGIONS

This option controls the list of regions that you want to scan
for the dynamic inventory. By default the script will only works within the 'us-east-1' region.

### Adding 'us-east-1' and 'us-east-2' for scanning.

REGIONS = ['us-east-1', 'us-east-2']

---------------------------------------------------

- SCAN_ALL_REGION

If you enable this option then the script will scan for instances in all aws regions. If this options is enabled it will
ignore the REGIONS value. By default this option will be set to false.

### Enabling All Region Scaning.

SCAN_ALL_REGION = True

---------------------------------------------------

- AWS Credentials

By default script will fetch aws credentials from .aws/credentials file. you can override this option by setting

```
ACCESS_KEY = 'YourAccessKey'  
SECRET_KEY = 'YourSecretKey'
```
