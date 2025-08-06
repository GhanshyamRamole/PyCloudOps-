import boto3

# Initialize RDS client
rds_client = boto3.client('rds', region_name='ap-south-1')  # change region as needed

# RDS MySQL configuration
db_instance_identifier = 'cloud'  # Unique name for the DB instance
db_instance_class = 'db.t3.micro'        # Free tier eligible
engine = 'mysql'
master_username = 'admin'                # Master username
master_password = 'Ghanshyam23' # Master password
allocated_storage = 20                   # 20 GB minimum for RDS MySQL

try:
    print("Creating RDS MySQL instance... This may take several minutes.")

    response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_instance_identifier,
        AllocatedStorage=allocated_storage,
        DBInstanceClass=db_instance_class,
        Engine=engine,
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        BackupRetentionPeriod=7,
        PubliclyAccessible=True,
        MultiAZ=False,
        StorageType='gp2',
        Port=3306,
        DBName='cloud',  # Optional: Default database name
        DeletionProtection=False
    )

    print("RDS MySQL creation started successfully!")
    print("DB Instance ARN:", response['DBInstance']['DBInstanceArn'])

except Exception as e:
    print("Error creating RDS MySQL:", e)

