import boto3
from datetime import datetime
from datetime import datetime, timezone

from datetime import datetime, timedelta

def get_ec2_running_hours(region):
    ec2 = boto3.client('ec2', region_name=region)
    now = datetime.utcnow()

    response = ec2.describe_instances()
    total_hours = 0

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                launch_time = instance['LaunchTime'].replace(tzinfo=None)
                run_time = now - launch_time
                hours = run_time.total_seconds() / 3600
                total_hours += hours

    return round(total_hours, 2)

def get_s3_storage_usage():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    total_size_bytes = 0

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            # Get total size of all objects in the bucket
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name)

            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_size_bytes += obj['Size']
        except Exception as e:
            print(f"⚠️ Could not access bucket {bucket_name}: {e}")

    total_gb = round(total_size_bytes / (1024 ** 3), 2)
    return total_gb







def get_rds_running_hours(region):
    client = boto3.client('rds', region_name=region)
    total_hours = 0
    now = datetime.now(timezone.utc)

    response = client.describe_db_instances()
    for db in response['DBInstances']:
        if db['DBInstanceStatus'] == 'available':
            launch_time = db['InstanceCreateTime']
            hours = (now - launch_time).total_seconds() / 3600
            total_hours += hours

    return round(total_hours, 2)


def get_lambda_usage(region):
    import boto3
    import datetime

    client = boto3.client('cloudwatch', region_name=region)

    # Get current month range
    now = datetime.datetime.utcnow()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now

    metrics = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'lambdaComputeUsage',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/Lambda',
                        'MetricName': 'Duration',
                        'Dimensions': [{'Name': 'FunctionName', 'Value': 'ALL'}]
                    },
                    'Period': 86400,  # Daily
                    'Stat': 'Average'
                },
                'ReturnData': True,
            }
        ],
        StartTime=start,
        EndTime=end
    )

    # Currently, AWS CloudWatch does not support metric math across ALL Lambda functions.
    # We’ll simulate a single metric view here. For real app, you’d need to query each function individually.

    # 👇 Workaround: Summing known values — we'll return 0.0 for demo/fallback
    compute_gb_seconds = 0.0

    return round(compute_gb_seconds, 2)
