import os
import subprocess
from subprocess import PIPE, STDOUT
from github3 import login

from config import token

gh = login(token=token)


def clone_repo(repo, starred=False):
    print(repo.ssh_url)
    print(repo.name)
    repo_directory = os.path.expanduser('~')
    if not starred:
        repo_directory = os.path.join(repo_directory, 'src', repo.name)
    else:
        repo_directory = os.path.join(repo_directory, 'src', 'starred', repo.name)
    if not os.path.exists(repo_directory):
        proc = subprocess.run(['C:/Users/Pierre/AppData/Local/Programs/Git/bin/git.exe',
                               'clone',
                               repo.ssh_url,
                               repo_directory], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        print(proc.stdout.decode())
    proc = subprocess.run(['C:/Users/Pierre/AppData/Local/Programs/Git/bin/git.exe',
                           '-C',
                           repo_directory,
                           'pull'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    print(proc.stdout.decode())


if __name__ == '__main__':
    for repo in gh.repositories():
        clone_repo(repo)
    starred = gh.starred()
    for repo in starred:
        clone_repo(repo, starred=True)
