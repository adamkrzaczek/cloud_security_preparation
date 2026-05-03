import boto3
from patterns import scan_dict

def run(session: boto3.Session, region, fix):
    client = session.client("lambda",region_name=region)
    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        for function in page.get("Functions",[]):
                env_vars = function.get("Environment",{}).get("Variables",{})
                if env_vars:
                    findings = scan_dict(env_vars)
                    if findings:
                        for finding in findings:
                            print(f"[!] Found {finding["pattern_name"]}; Severity {finding["severity"]}; location {finding["location"]} offset {finding["offset"]}")
                            if fix:
                                print(f"[!] Requires manual fix")
