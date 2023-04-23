# -*- coding: utf-8 -*-

# write a python script  have those functions
#    

import os
import shutil
import json
def copy_port_template(port_template_path, ports_path, new_port_name):
    shutil.copytree(port_template_path, os.path.join(ports_path, new_port_name),dirs_exist_ok =True)

def change_vcpkg_json(ports_path, port_name,url):
    vcpkg_json_path = os.path.join(ports_path, port_name, "vcpkg.json")
    with open(vcpkg_json_path, "r") as f:        
        baseline_json = json.loads(f.read())
        baseline_json['name']=port_name
        baseline_json['description']=f"a simplylive {port_name} library"
        baseline_json['homepage']=url

    with open(vcpkg_json_path, "w") as f:        
        f.write(json.dumps(baseline_json,indent=4))

def makeNew_vcpkg_json(ports_path, port_name,url):
    vcpkgJosn={
    "name": f"{port_name}",
    "version": "1.0.0",
    "description": f"a simplylive {port_name} library",
    "homepage": f"{url}",
}
    
    vcpkg_json_path = os.path.join(ports_path, port_name, "vcpkg.json")
    with open(vcpkg_json_path, "w") as f:
        f.write(json.dumps(vcpkgJosn,indent=4))

def replace_url_in_portfileCMake(ports_path, port_name, new_url):
    portfile_cmake_path = os.path.join(ports_path, port_name, "portfile.cmake")
    with open(portfile_cmake_path, "r") as f:
        content = f.read()
    content = content.replace("CURRENT_BITBUCKET_REPO_GIT_URL", new_url)
    with open(portfile_cmake_path, "w") as f:
        f.write(content)


def create_version_file(port_name, version_info):    
    first_letter = port_name[0]
    version_file_path = os.path.join("versions", f"{first_letter}-", f"{port_name}.json")
    os.makedirs(os.path.dirname(version_file_path), exist_ok=True)
    with open(version_file_path, "w") as f:
        json.dump(version_info, f)


def MakeNewPort(port_name,url):
    port_name= port_name.lower()
    ports_path = "./ports"
    if not os.path.exists(ports_path):
        os.makedirs(ports_path)
    copy_port_template("./port_template", ports_path, port_name)    
    change_vcpkg_json(ports_path, port_name,url)
    replace_url_in_portfileCMake(ports_path, port_name, url)


    create_version_file(port_name, {"version": "0.0.1","port-version":0,"git-tree":""})
#1. copy port_template into ports
#2. then rename the folder to "YOUR_PORT"
#3. change the value of "name" in the vcpkg.json
#4. use your correct url replace 'CURRENT_BITBUCKET_REPO_GIT_URL' in the portfile.cmake
#5. create versions database file version/<first letter of port>-/<name of port>.json



MakeNewPort('X', 'https://bitbucket.org/x-vcpkg/x-vcpkg.git')