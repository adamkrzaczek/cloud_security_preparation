import boto3

def run(session: boto3.Session,region):
    sm = session.client("secretsmanager",region_name=region)
    paginator = sm.get_paginator("list_secrets")
    for page in paginator.paginate():
        secret_list = page.get("SecretList",[])
        for secret in secret_list:
            arn = secret.get("ARN","")
            name = secret.get("Name","")
            resource = sm.get_resource_policy(SecretId=arn)
            policy = resource.get("ResourcePolicy")
            if not policy:
                print(f"[!] No resource policy attached to secret {name}")