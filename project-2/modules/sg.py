def create_security_group(name, desc, vpc_id, ports):
    ec2 = get_client('ec2')
    sg = ec2.create_security_group(
        GroupName=name,
        Description=desc,
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']
    for port in ports:
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[{
                'IpProtocol': 'tcp',
                'FromPort': port,
                'ToPort': port,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }]
        )
    return sg_id

