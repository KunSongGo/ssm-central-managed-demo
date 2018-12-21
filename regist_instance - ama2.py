#!/usr/bin/python

import os
import urllib2
import json
import commands
import re
import boto3
from boto3 import session

#Retrieving Instance Details such as Instance ID and Region from EC2 metadata service

instance_details = json.loads(urllib2.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read())

instanceid=instance_details['instanceId']
REGION=instance_details['region']

# Getting the AWS credentials from the IAM role

session = session.Session()
credentials = session.get_credentials()

def Activation(InstanceID):

        #Getting Activation ID and Code from parameter store
        ssm = boto3.client('ssm',region_name=REGION)

        activation_id = ssm.get_parameter(Name='ActivationId')
        ActivationID=activation_id['Parameter']['Value']
        activation_code = ssm.get_parameter(Name='ActivationCode')
        ActivationCode=activation_code['Parameter']['Value']

        # Registering Instance to Activation and storing ManagedInstanceID for tagging

        status_stop_service, Output_stop_service =commands.getstatusoutput("sudo systemctl stop amazon-ssm-agent")

        cmd="sudo amazon-ssm-agent -register -y -code %s -id %s -region %s"%(ActivationCode,ActivationID,REGION)

        status, output = commands.getstatusoutput(cmd)
        m = re.search('(mi-)\w{17}',output.splitlines()[-1])

        ManagedInstanceID=m.group(0)

        if status==0:

                status_start_service, Output_start_service =commands.getstatusoutput("sudo systemctl start amazon-ssm-agent")

        print ManagedInstanceID

        # Creating Tag for ManagedInstanceID tag
        create_tags = ec2.create_tags(Resources=[str(InstanceID)],Tags=[{'Key':'managedinstanceid','Value':ManagedInstanceID}])

# Checking if Instance already has ManagedInstanceID Tag

ec2=boto3.client('ec2',region_name=REGION)

ec2_attached_tags = ec2.describe_instances(Filters=[{'Name': 'tag-key','Values': ['managedinstanceid']}],InstanceIds=[instanceid])

if not ec2_attached_tags['Reservations']:
	Activation(instanceid)
else:
	print "Instance is already registered to an Activation/Account"