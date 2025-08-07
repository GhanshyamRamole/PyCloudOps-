from utils.aws_session import get_client
import time

def create_rds_subnet_group(name, subnet_ids, description="RDS subnet group"):
    rds = get_client("rds")
    try:
        rds.create_db_subnet_group(
            DBSubnetGroupName=name,
            DBSubnetGroupDescription=description,
            SubnetIds=subnet_ids,
            Tags=[{"Key": "Name", "Value": name}]
        )
        print(f"[RDS] Created subnet group: {name}")
    except rds.exceptions.DBSubnetGroupAlreadyExistsFault:
        print(f"[RDS] Subnet group '{name}' already exists. Skipping.")

def create_rds_instance(
    db_identifier,
    db_name,
    master_username,
    master_password,
    db_subnet_group_name,
    vpc_security_group_ids,
    instance_class="db.t3.micro",
    engine="mysql",
    allocated_storage=20,
    public_access=True
):
    rds = get_client("rds")
    
    try:
        rds.create_db_instance(
            DBName=db_name,
            DBInstanceIdentifier=db_identifier,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            DBInstanceClass=instance_class,
            Engine=engine,
            AllocatedStorage=allocated_storage,
            VpcSecurityGroupIds=vpc_security_group_ids,
            DBSubnetGroupName=db_subnet_group_name,
            PubliclyAccessible=public_access,
            Tags=[
                {"Key": "Project", "Value": "DevProj1"},
                {"Key": "Environment", "Value": "Development"}
            ]
        )
        print(f"[RDS] Creating RDS instance '{db_identifier}'...")

        # Wait for instance to become available
        waiter = rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=db_identifier)
        print(f"[RDS] RDS instance '{db_identifier}' is now available.")

    except rds.exceptions.DBInstanceAlreadyExistsFault:
        print(f"[RDS] RDS instance '{db_identifier}' already exists. Skipping.")

def get_rds_endpoint(db_identifier):
    rds = get_client("rds")
    response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
    return response["DBInstances"][0]["Endpoint"]["Address"]

