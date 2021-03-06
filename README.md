# docker-registry-explorer
This tool was inspired by [this article](https://www.notsosecure.com/anatomy-of-a-hack-docker-registry/).
I wasn't satisfied of the other tools I found so i created my own.

### What should you use it for
Test the api supported for the target Docker registry.
Explore, download and get infos from the repositories.
**Authentication is also supported.**

## Usage

*Right now api v1 is not supported, on 'list', 'tags' and 'download' functions.*

```shell
usage: docker_registry_explorer.py [-h] {list,tags,download,apitest} ...

Docker Private Registry Explorer & Downloader
Simple Python tool to download images from Docker Private Registries.
Inspired by https://www.notsosecure.com/anatomy-of-a-hack-docker-registry/
                     __       __
                     '.'--.--'.-'
       .,_------.___,   \' r'
       ', '-._a      '-' .'
        '.    '-'Y \._  /
          '--;____'--.'-,
       snd /..'       '''
        

optional arguments:
  -h, --help            show this help message and exit

actions:
  {list,tags,download,apitest}
    list                list repositories from registry
    tags                show tags associated with a repo
    download            print manifest and download images from given repository
    apitest             automatic test api version

```

#### Example

List all repositories :
```shell
./docker_registry_explorer.py list -d http://docker.regist.my -a test:test -v2
```
