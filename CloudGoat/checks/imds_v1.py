from botocore.exceptions import ClientError

def run(session, region: str, fix_flag: bool):
        ec2 = session.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_instances")
        for page in paginator.paginate():
            for reservation in page.get("Reservations",[]):
                for instance in reservation.get("Instances",[]):
                    instance_id = instance.get('InstanceId')
                    metadata_option = instance.get("MetadataOptions",{})
                    http_token = metadata_option.get("HttpTokens")
                    if http_token == "optional":
                        print(f"[!] {region}: IMDSv1 ENABLED on {instance_id} ({instance.get('InstanceType')})")
                        if fix_flag :
                            fix(ec2,instance_id)

def fix(ec2,instanceId: str):
    try:
        ec2.modify_instance_metadata_options(InstanceId=instanceId,HttpTokens="required")
        print(f"[+] FIXED {instanceId}. Now it use IMDSv2")
    except ClientError as e:
        error = e.response.get("Error",{})
        error_msg = error.get("Message","Unknown AWS    Error")
        print(f"[X] Couldn't fix the issue: {instanceId}: {error_msg}")
