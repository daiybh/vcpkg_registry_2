# 这个函数有以下功能
# 遍历 ports 文件夹
# read all ports
# read all portfile.cmake
# get sections 'vcpkg_from_git' or 'vcpkg_from_github' or 'vcpkg_from_bitbucket'
# the sections include REPO REF SHA512 HEAD_REF
#  update REF SHA512  form REPO 

import json
import pathlib,re

import argparse
import time
import requests
import version_parser
import git
import os

from checkbitbucket import getLastCommit

def parse_vcpkg_from(portfile,beginKey="vcpkg_from_github(",endKey="vcpkg_from_github("):
    metaDataList=[]
    end=0
    while True:
        begin = portfile.find(beginKey,end)
        if begin == -1:
            break

        begin += len(endKey)
        end = portfile.find(")", begin)
       

        interest = portfile[begin:end]
        splits = re.split(' |\n', interest)
        items = []
        for split in splits:
            split = split.strip()
            if len(split) > 0:
                items.append(split)

        if len(items) % 2 != 0:
            break

        ret = {}
        for i in range(0, len(items), 2):
            ret[items[i]] = items[i + 1]
        metaDataList.append(ret)
    return metaDataList

#https://api.bitbucket.org/2.0/repositories/id4tv/jpeg/commit
def github_get_latest_commit(repo, head):
    r = requests.get(f"https://api.github.com/repos/{repo}/commits/{head}", proxies={
                     'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'})
    j = r.json()
    return j['sha']

def bitbucket_get_last_commit(repo,head):
    #git@bitbucket.org:id4tv/jpeg.git
    name = repo.split('/')[-1].split('.')[0]
    return getLastCommit(repo_slug=name,head=head)

def parse_vcpkgGitForm(portfile):
    #githubMeta=parse_vcpkg_from(portfile)
    gitMeta=parse_vcpkg_from(portfile,beginKey='vcpkg_from_git(',endKey='vcpkg_from_git(')
    #bibucketMeta=parse_vcpkg_from(portfile,beginKey='vcpkg_from_bitbucket(',endKey='vcpkg_from_bitbucket(')
    allMeta=[]
    #allMeta.extend(githubMeta)
    allMeta.extend(gitMeta)
    #allMeta.extend(bibucketMeta)
    return allMeta

def updatePortVersion(portName,version,git_tree_object_id):
    port_version_folder="./versions/" + portName[0] + "-/"
    port_version_path=port_version_folder + portName + ".json"

    if not os.path.exists(port_version_folder):
        os.makedirs(port_version_folder)  
        
    with open(port_version_path,'w') as f:    
        port_version_json={
        "versions": [
        {
            "version": "1.0.0",
            "git-tree": "6dc64b4368b163307641e0bfd33c0938b2c65d23"
        }
        ]
    }
        port_version_json['versions'].append(
                {"version-string": str(version), "git-tree": git_tree_object_id})
        f.write(json.dumps(port_version_json,indent=4))

parser = argparse.ArgumentParser(description='Auto update vcpkg private registry repo')
parser.add_argument('-f', action='store_true', help="Force update all files, even the local portfile.cmake already up-to-date.") 
args = parser.parse_args() 

force_update = args.f

def UpdatePort(port):
    vcpkg_json_path = port.joinpath("vcpkg.json")
    portfile_cmake_path = port.joinpath("portfile.cmake")
    if vcpkg_json_path.exists() and portfile_cmake_path.exists():
        print("Updating " + port.name)
        # Parse vcpkg_from_github
        portfile_str = portfile_cmake_path.read_text()
        github_meta = parse_vcpkgGitForm(portfile_str)
        if github_meta is None:
            return
        bFirst=True
        strVersion=''
        for meta in github_meta:            
            cur_ref=meta['REF']
            latest_commit = bitbucket_get_last_commit(meta['URL'], meta['HEAD_REF'])
            
            if latest_commit ==cur_ref  and not force_update:
                print(f"- {meta['URL']} Already up-to-date.")
                bFirst=False
                continue

            # Calculate Latest SHA512
            #latest_sha512 = github_get_archive(github_repo, latest_commit)
            print(f"- Latest commit {latest_commit}")
            #print(f"- Latest sha512 = {latest_sha512}")

            # Update portfile.cmake
            #portfile_str = portfile_str.replace(github_sha, latest_sha512)
            portfile_str = portfile_str.replace(cur_ref, latest_commit)
            portfile_cmake_path.write_text(portfile_str)

            # Update vcpkg.json
            if bFirst:
                vcpkg_json = json.loads(vcpkg_json_path.read_text())
                version = version_parser.Version(vcpkg_json['version'])
                version._build_version += 1
                vcpkg_json['version'] = str(version)
                strVersion=str(version)
                vcpkg_json_path.write_text(json.dumps(vcpkg_json,indent=4))

            bFirst=False
        if strVersion=='':
            return
        # Update Git
        try:
            git_repo.git.add(port.absolute()) 
            git_repo.git.commit(m="Update " + port.name)
            git_repo.remote().push()
        except:
            pass
        git_tree_object_id = str(git_repo.rev_parse("HEAD:ports/" + port.name))
        print(f"- Latest git-tree = {git_tree_object_id}")

        # Update Versions
        updatePortVersion(port.name,strVersion,git_tree_object_id)

        # Update Baseline
        baseline_path = pathlib.Path("./versions/baseline.json")
        baseline_json = json.loads(baseline_path.read_text())
        if port.name not in baseline_json['default']:
            baseline_json['default'][port.name] = {}
        baseline_json['default'][port.name]['baseline'] = strVersion
        baseline_path.write_text(json.dumps(baseline_json,indent=4))
        
        time.sleep(5)

git_repo = git.Repo("./")
ports_folder = pathlib.Path("./ports")
for port in ports_folder.iterdir():
    UpdatePort(port)
    try:
        print("")
    except Exception as e:
        print(f"Error: {port.name}  {e}")

# Update Git Root
try:
    git_repo.git.add(".") 
    git_repo.git.commit(m="Update Root")
    git_repo.remote().push()
except:
    pass
print("Complete")