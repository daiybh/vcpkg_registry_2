

import pathlib
import requests
import sys
import json
import BTconfig
'''
username is the 
password is the APPPassword
'''
username=BTconfig.username
password=BTconfig.password

projectKeys =['SimSer','VID','VEN']

import shutil,os
def makeNewPort(full_name,url):
    name= full_name.split('/')[-1]
    print(name,full_name,url)
    port_path = pathlib.Path("./ports/"+name)
    if os.path.exists(port_path):
        return
    
    shutil.copytree('port_template', port_path)

    vcpkg_json_path = port_path.joinpath("vcpkg.json" )
    portfile_cmake_path = port_path.joinpath("portfile.cmake")

    vcpkg_json = json.loads(vcpkg_json_path.read_text())
    vcpkg_json['name']=name
    vcpkg_json['homepage']=url
    vcpkg_json['description']=f'a simplylive {name} library'
    vcpkg_json_path.write_text(json.dumps(vcpkg_json,indent=4))

    portfile_str = portfile_cmake_path.read_text()

    portfile_str = portfile_str.replace('CURRENT_BITBUCKET_REPO_GIT_URL', url)
    portfile_cmake_path.write_text(portfile_str)
    



    
def getRepo(projectKey):
    nextURL=f'https://bitbucket.org/api/2.0/repositories/id4tv?q=project.key="{projectKey}"'    

    while len(nextURL) >10:
        r = requests.get(nextURL,   auth=(username, password))    
        repos = r.json() 
        nextURL=repos.get('next','')
        for item in repos['values']:
            for cloneItem in item['links']['clone']:        
                if cloneItem['name']!='ssh':
                    continue

                makeNewPort(item['full_name'],cloneItem['href'])
                    
                
for projectKey in projectKeys:    
    getRepo(projectKey=projectKey)
