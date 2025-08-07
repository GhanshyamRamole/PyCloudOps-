def launch_ec2(ami_id, key, subnet_id, sg_ids, user_data_script):
    ec2 = get_client('ec2')
    instance = ec2.run_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        KeyName=key,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=sg_ids,
        SubnetId=subnet_id,
        UserData=user_data_script,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'Ubuntu Linux EC2'}]
        }]
    )
    return instance['Instances'][0]['InstanceId']

