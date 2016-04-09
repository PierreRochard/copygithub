import os
import subprocess
from subprocess import PIPE, STDOUT
import platform

from github3 import login
import keyring

token = keyring.get_password('github', 'token')

gh = login(token=token)

if platform == 'Windows':
    git_command = 'C:/Users/Pierre/AppData/Local/Programs/Git/bin/git.exe'
else:
    git_command = 'git'


def clone_repo(repo, starred=False):
    print(repo.html_url)
    print(repo.name)
    repo_directory = os.path.expanduser('~')
    if not starred:
        repo_directory = os.path.join(repo_directory, 'github-src', repo.name)
    else:
        repo_directory = os.path.join(repo_directory, 'github-src', 'starred', repo.name)
    if not os.path.exists(repo_directory):
        proc = subprocess.run([git_command, 'clone', repo.html_url, repo_directory],
                              stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        print(proc.stdout.decode())
    proc = subprocess.run([git_command, '-C', repo_directory, 'pull'],
                          stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    print(proc.stdout.decode())


if __name__ == '__main__':
    for repo in gh.iter_all_repos():
        clone_repo(repo)
    starred = gh.starred()
    for repo in starred:
        clone_repo(repo, starred=True)
