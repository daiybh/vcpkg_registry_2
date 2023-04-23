# how to

## Create a Port

1. Standard 

    1. Create a Folder named "YOUR_PORT" in ports

        ex: video-x    then ports/video-x

    2. Create a file named portfile.cmake in this directory.
        Create a file named vcpkg.json in this directory.

        ex :  ports/video-x/portfile.cmake
        ex :  ports/video-x/vcpkg.json

2. Simply :
    1. copy port_template into ports
    2. then rename the folder to "YOUR_PORT"
    3. change the value of "name" in the vcpkg.json
    4. use your correct url replace 'CURRENT_BITBUCKET_REPO_GIT_URL' in the portfile.cmake
    5. create versions database file version/<first letter of port>-/<name of port>.json
    

## Check new Port

 now can check the port if can  work.

 run this command in this registry folder.

``` cmd
cd %current Registry Folder%

vcpkg install video-x --overlay-ports=ports/video-x
```

## Adding a new version

1. Each port in a registry should exist in the versions directory as <first letter of port>-/<name of port>.json

    ex: versions/v-/video-x.json

2. Once you've finished your testing, you'll need to make sure that the directory as it is is under git's purview. You'll do this by creating a temporary commit:

    ```
    > git add ports/video-x
    > git commit -m 'temporary commit'
    ```

3. Then, get the git tree ID of the directory:

    ```
    > git rev-parse HEAD:ports/video-x
    73ad3c823ef701c37421b450a34271d6beaf7b07
    ```

4. Then, you can add this version to the versions database. At the top of your **versions/v-/video-x.json**
you can add (assuming you're adding version 2.6.3#0):

    ``` json
    {
        "versions": [
            {
            "version": "2.6.3",
            "port-version": 0,
            "git-tree": "73ad3c823ef701c37421b450a34271d6beaf7b07"
            },
            {
            "version": "2.6.2",
            "port-version": 0,
            "git-tree": "67d60699c271b7716279fdea5a5c6543929eb90e"
            }
        ]
    }
    ```

5. Then, you'll want to modify your versions/baseline.json with your new version as well:

    ``` json
    {
        "default": {
            "video-x": {
            "baseline": "2.6.3",
            "port-version": 0
            },
            "port-b": {
            "baseline": "19.00",
            "port-version": 2
            }
        }
    }
    ```

6. and amend your current commit:

    ``` cmd
    > git commit --amend
    ```

## Finally

    push to remote.
    