#!/bin/sh
yum update -y 
yum install python-pip -y  
yum install python2-boto3 -y 
curl https://raw.githubusercontent.com/KunSongGo/ssm-central-managed-demo/master/regist_instance-ama2.py | python