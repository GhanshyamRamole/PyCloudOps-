from utils.aws_session import get_client

def create_vpc(cidr, name):
    ec2 = get_client('ec2')
    vpc = ec2.create_vpc(CidrBlock=cidr)
    vpc_id = vpc['Vpc']['VpcId']
    ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": name}])
    return vpc_id

