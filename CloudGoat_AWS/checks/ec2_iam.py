import boto3

def run(session: boto3.Session, region: str, fix: bool):
    ec2 = session.client("ec2",region_name=region)
    iam = session.client("iam",region_name=region)
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations",[]):
            for instance in reservation.get("Instances",{}):
                intance_id = instance.get("InstanceId","")
                iam_profile = instance.get("IamInstanceProfile",{})
                if not iam_profile: 
                    continue
                profile = iam_profile.get("Arn","").split("/")[-1]
                role_info = iam.get_instance_profile(InstanceProfileName=profile)
                roles = role_info["InstanceProfile"]["Roles"]
                for role in roles:
                    role_name = role["RoleName"]
                    #Check inline policies
                    inline = iam.list_role_policies(RoleName=role_name)
                    for policy in inline.get("PolicyNames",[]):
                        policies = iam.get_role_policy(RoleName=role_name, PolicyName=policy)

                        if "*" in str(policies.get("PolicyDocument",{})):
                            print(f"[!] Wildcard found in {policy}")
                            if fix:
                                print(f"[!] Requires manual fix")
                    attached = iam.list_attached_role_policies(RoleName=role_name)
                    for policy in attached.get("AttachedPolicies",[]):
                        if "AdministratorAccess" in policy.get("PolicyArn",""):
                            print(f"[!] Admin policy attached {policy["PolicyArn"]}") # type: ignore
                        version = iam.get_policy(PolicyArn=policy.get("PolicyArn",""))["Policy"].get("DefaultVersionId","")
                        if "*" in str(iam.get_policy_version(PolicyArn=policy.get("PolicyArn",""),VersionId=version)):
                            print(f"[!] Wildcard found in {policy}")
                            if fix:
                                print(f"[!] Requires manual fix")
                        
