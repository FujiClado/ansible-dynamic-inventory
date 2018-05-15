#!/usr/bin/env python3

import boto3
import json


########################################################
# Mentions your regions as a list. The script will only
# creates group of instances running on this regions 
########################################################

REGIONS = ['us-east-1']


########################################################
# put SCAN_ALL_REGION = True , if you want to this script
# to scan for all regions for instances.
########################################################

SCAN_ALL_REGION =  False


########################################################
# Specify your accessKey and secretKey 
# leave it as "None" for fetching from .aws/credentials
########################################################

ACCESS_KEY = ''
SECRET_KEY = ''


########################################################
# This dictionary picks default user name from the AMI
# description.
########################################################

AMI_USERS = {
    'Centos':'centos',
    'Amazon':'ec2-user',
    'Debian':'admin',
    'Fedora':'fedora',
    'RHEL': 'ec2-user',
    'SUSE':'ec2-user',
    'Ubuntu':'ubuntu'
    
  } 



inventory = { 'all': 
                 { 'hosts': [],
                   'vars': 
                    { 'ansible_ssh_common_args':'-o StrictHostKeyChecking=no'} },
               '_meta': 
                  {
                    'hostvars': {},
                    
                  }
              }



def find_user(description):
    for os in AMI_USERS:
      if os in description:
        return AMI_USERS[os]
  

if SCAN_ALL_REGION:
  if ACCESS_KEY and SECRET_KEY:
    scan_all_client = boto3.client('ec2',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
  else:  
    scan_all_client = boto3.client('ec2')  
    
  REGIONS = [ region in client.describe_regions()['Regions'] ]

for region in REGIONS:
  if ACCESS_KEY and SECRET_KEY:
    ec2_client = boto3.resource('ec2',region_name=region,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
  else:
    ec2_client = boto3.resource('ec2') 
  
  for instance in ec2_client.instances.all():
    for tag in instance.tags:
      # Scanning for instance with a tag with key 'ansible'.
      if tag['Key'].lower() == 'ansible':
        # Fetching the image meta data of the instance AMI.
        image = ec2_client.Image(instance.image_id)
        ssh_host = instance.public_ip_address
        ssh_user = find_user(image.description)
        # Checking whether 'ansible' tag contains mutilple group names
        # separated by colons.
        groups = tag['Value'].split(':')
        inventory['all']['hosts'].append(ssh_host)
        inventory['_meta']['hostvars'][ssh_host] = {
          'ansible_port':22, 
          'ansible_user': ssh_user
        }
        for group in groups:
          if group not in inventory:
            inventory[group] = []
            inventory[group].append(ssh_host)
          else:  
            inventory[group].append(ssh_host)  

print(json.dumps(inventory,indent=2))  
