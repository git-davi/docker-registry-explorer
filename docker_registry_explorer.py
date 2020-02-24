#!/bin/python3
import requests
import json
import argparse

from requests.auth import HTTPBasicAuth
from tqdm import tqdm



parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, 
        description=
        '''
Docker Private Registry Explorer & Downloader
Simple Python tool to download images from Docker Private Registries.
Inspired by https://www.notsosecure.com/anatomy-of-a-hack-docker-registry/
                     __       __
                     '.'--.--'.-'
       .,_------.___,   \\' r'
       ', '-._a      '-' .'
        '.    '-'Y \._  /
          '--;____'--.'-,
       snd /..'       \'\'\'
        ''')

action = parser.add_subparsers(title="actions", dest="action")

action_ls = action.add_parser("list", help="list repositories from registry")
action_ls.add_argument("-a", "--auth", help="user:pass for authentication")
action_ls.add_argument("-d", "--dest", help="destination ip or domain, format : [http or https]://<ip or domain>", required=True)
action_ls.add_argument("-v", "--vapi", help="api version you want to use ex. [v1 , v2]", required=True)

action_st = action.add_parser("tags", help="show tags associated with a repo")
action_st.add_argument("-a", "--auth", help="user:pass for authentication")
action_st.add_argument("-r", "--repo", help="the name of the repository that you want to download", required=True)
action_st.add_argument("-d", "--dest", help="destination ip or domain, format : [http or https]://<ip or domain>", required=True)
action_st.add_argument("-v", "--vapi", help="api version you want to use ex. [v1 , v2]", required=True)

action_dl = action.add_parser("download", help="print manifest and download images from given repository")
action_dl.add_argument("-a", "--auth", help="user:pass for authentication")
action_dl.add_argument("-r", "--repo", help="the name of the repository that you want to download", required=True)
action_dl.add_argument("-d", "--dest", help="destination ip or domain, format : [http or https]://<ip or domain>", required=True)
action_dl.add_argument("-v", "--vapi", help="api version you want to use ex. [v1 , v2]", required=True)
action_dl.add_argument("-t", "--tag", help="the tag for the repo version you have decided to download", required=True)

action_at = action.add_parser("apitest", help="automatic test api version")
action_at.add_argument("-a", "--auth", help="user:pass for authentication")
action_at.add_argument("-d", "--dest", help="destination ip or domain, format : [http or https]://<ip or domain>", required=True)


#------------------------------------------------------------------------------------------

def error(data):
    print("Something went wrong\n\n")
    print(json.dumps(data, indent=2))
    exit(1) 


def make_request(url, auth) :
    try :
        r = requests.get(url, auth=auth)
    except :
        print("Connection failed, check url")
        exit(1)
    return r



def action_list() :
    r = make_request(args.dest+"/"+ args.vapi+"/_catalog", auth=auth) 
    if r.status_code != 200 :
        error(r.json())
    print("Here is the repos list")
    print(json.dumps(r.json(), indent=2))


def action_download() :
    index = 0
    suffix = ".tar.gz"
    manifest_url = args.dest+"/"+args.vapi+"/"+args.repo+"/manifests/"+args.tag
    blobs_url = args.dest+"/"+args.vapi+"/"+args.repo+ "/blobs/"

    r = make_request(manifest_url, auth=auth)
    data = r.json()
    
    if r.status_code != 200 :
       error(data) 

    print("-------------------------------------------------- Begin Manifest File --------------------------------------------------\n\n")
    print(json.dumps(data, indent=2))
    print("-------------------------------------------------- End Manifest File --------------------------------------------------\n\n")
    print("Downloading ...")

    for blob in tqdm(data["fsLayers"]):
        u = blobs_url + blob["blobSum"]
        blob_r = make_request(u, auth=auth)
        if blob_r.status_code != 200 :
            error(blob_r.json())
        with open(args.repo + str(index) + suffix, "wb") as f:
            f.write(blob_r.content)
        index += 1
    print("Finished")
    

def show_tags() :
    r = make_request(args.dest+"/"+args.vapi+"/"+args.repo+"/tags/list", auth=auth)
    if r.status_code != 200 :
        error(r.json())
    print("Tags list :\n\n")
    print(json.dumps(r.json(), indent=2))



def action_apitest() :
    versions = ("/v1/", "/v2/")
    for v in versions :
        r = make_request(args.dest+v, None)
        if r.status_code != 404 :
            print("The registry seems to work with api : "+v[1:-1])



auth = None
switch = {
        "list": action_list,
        "download": action_download,
        "apitest": action_apitest,
        "tags": show_tags
        }

args = parser.parse_args()
if args.action == None :
    print("Missing arguments, -h for help")
    exit(1)

if args.auth != None :
    user, passwd = args.auth.split(":")
    auth = HTTPBasicAuth(user, passwd)

switch[args.action]()
exit(0)
