import boto3
import base64
from patterns import scan_text

def run(session: boto3.Session,region: str, fix: bool):
    ec2 = session.client('ec2',region_name=region)
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get('Reservations',[]):
            for instance in reservation.get('Instances',[]):
                instance_id = instance.get('InstanceId','Unknown')
                attributes = ec2.describe_instance_attribute(InstanceId=instance_id,Attribute='userData')
                data = attributes.get('UserData',{}).get('Value')
                try:
                    data_decode = base64.b64decode(data).decode('utf-8',errors = 'ignore')
                except Exception as e:
                    print(f"[!] ERROR: {e}")
                findings=scan_text(data_decode)
                if findings:
                    for finding in findings:
                        print(f"[!] Found {finding["pattern_name"]}; severity - {finding["severity"]}; Preview: {finding["preview"]}")
                        if fix:
                            print(f"[!] Requires manual fix")