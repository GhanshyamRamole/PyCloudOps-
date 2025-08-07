from modules import networking, security_group, ec2
from dotenv import load_dotenv
from modules import rds
import os

load_dotenv()

# Get values from .env
vpc_cidr = os.getenv("VPC_CIDR")
public_subnet_cidr = os.getenv("PUBLIC_SUBNET_CIDR")
private_subnet_cidr = os.getenv("PRIVATE_SUBNET_CIDR")
ami_id = os.getenv("EC2_AMI_ID")
key_name = os.getenv("EC2_KEY_NAME")

# Step 1: Create VPC
vpc_id = networking.create_vpc(vpc_cidr, "dev_proj_1")
print(f"[VPC] Created: {vpc_id}")

# Step 2: Security Groups
sg_ssh_http = security_group.create_security_group("SG-SSH-HTTP", "Enable SSH(22) and HTTP(80)", vpc_id, [22, 80])
sg_api = security_group.create_security_group("SG-API", "Enable port 5000", vpc_id, [5000])
print(f"[SG] SSH/HTTP: {sg_ssh_http}, API: {sg_api}")

# Step 3: Launch EC2
user_data_script = open("template/ec2_install_apache.sh").read()
instance_id = ec2.launch_ec2(ami_id, key_name, "subnet-xyz", [sg_ssh_http, sg_api], user_data_script)
print(f"[EC2] Launched: {instance_id}")

# Add other modules similarly (ALB, Target Group, RDS, etc.)


# RDS setup
db_subnet_group_name = "dev_proj_1_rds_subnet_group"
subnet_ids = ["subnet-abc", "subnet-def"]  # Replace with actual public/private subnet IDs
rds.create_rds_subnet_group(db_subnet_group_name, subnet_ids)

rds.create_rds_instance(
    db_identifier="mydb",
    db_name=os.getenv("MYSQL_DBNAME"),
    master_username=os.getenv("MYSQL_USERNAME"),
    master_password=os.getenv("MYSQL_PASSWORD"),
    db_subnet_group_name=db_subnet_group_name,
    vpc_security_group_ids=[sg_ssh_http]  # or your RDS-specific SG
)

endpoint = rds.get_rds_endpoint("mydb")
print(f"[RDS] RDS endpoint: {endpoint}")

