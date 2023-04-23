
import requests
import json
import BTconfig
'''
username is the 
password is the APPPassword
'''
username=BTconfig.username
password=BTconfig.password

workspace='id4tv'

def getLastCommit(repo_slug, head='HEAD'):
    
    nextURL=f'https://bitbucket.org/api/2.0/repositories/id4tv?q=project.key="SSM"'    
    icount=2
    while icount>0:
        nextURL=f'https://bitbucket.org/api/2.0/repositories/{workspace}/{repo_slug}/commits/{head}'        
        r = requests.get(nextURL,   auth=(username, password))
        repos = r.json()
        try:
            for repo in repos['values']:        
                return repo['hash']
        except:
            head='HEAD'
        icount-=1


if __name__ == '__main__':
    repo_slug='jpeg'
    getLastCommit(repo_slug)

