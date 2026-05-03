import argparse
from utils import get_regions,get_session

#IMPORT CHECKS
from checks import imds_v1, userData, lambdas
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix",action="store_true",help="Automatic Fix")
    parser.add_argument("--region",nargs="+",default=["us-east-1"], help="List regions to check")

    return parser.parse_args()

def main():
    args = get_args()
    session = get_session()
    regions = get_regions(args.region)
    for region in regions:
        
        #Check 1: IMDSv1
        #imds_v1.run(session,region,args.fix)
        #userData.run(session,region,args.fix)
        lambdas.run(session,region,args.fix)

if __name__ == "__main__":
    main()