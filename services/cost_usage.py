import boto3
import datetime
from botocore.exceptions import ClientError

def fetch_cost_by_service(region):
    client = boto3.client('ce', region_name=region)

    today = datetime.date.today()
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    try:
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DataUnavailableException':
            print("⚠️ Cost data is not yet available. Please wait a bit and try again.")
        else:
            print(f"❌ Unexpected AWS error: {e}")
        return [], 0.0

    data = []
    total = 0.0
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        total += cost
        data.append((service, cost))

    return data, total
