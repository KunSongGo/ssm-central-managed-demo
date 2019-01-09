# ssm-central-managed-demo:
This is a demo usage for a solution explained in this page :
- https://aws.amazon.com/blogs/mt/centralized-management-of-multiple-accounts-and-cross-platform-ec2-instances-using-aws-systems-manager/

# Demo step: 
1. Run AWS CLI command to generate an activation ID and code : 

$ aws ssm create-activation --iam-role IAM-ROLE-FOR-SSM-INSTANCE  --registration-limit 100 --expiration-date 2019-01-19T00:00 --default-instance-name AGENCEY-ACCOUNTS

{
    "ActivationCode": "xxxxxxxxxxx+4Ok",
    "ActivationId": "xxxxx-xxxx-xxxxx-xxxxx-xxxxxxxx"
}

2. Deploy "central-account-ssm-tag-manager.yaml" template in central management account and enter two demo agency account ids at stack creation. 

3. Deploy "agency-account-setup.json" in agency account and enter the activate id+code with central account id+region at stack creation 

4. Deploy "agency-account-instance-luanches.json" in agency account in eu-west-1 region to launch linux instances. Deploy "agency-account-instance-luanches-win.json" to launch windows instances. Instances will be registered to central account SSM.

5. Deploy "agency-account-ssm-ec2-tag-collector.yaml" in agency account to create lambda to send tags to central account 


Please note that "agency-account-instance-luanches.json" file contains image id for amazon linux 2 image in eu-west-1 region, if you deploy this script in other regions, please change them to image ids in corresponding regions. 
