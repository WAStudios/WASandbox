# WAStudio/get_dependencies.py

import os
import git  # Requires GitPython: pip install GitPython

def ensure_repo(repo_url, clone_path):
    if not os.path.exists(clone_path):
        #print(f"Cloning {repo_url} into {clone_path}...")
        git.Repo.clone_from(repo_url, clone_path)
    else:
        #print(f"{clone_path} already exists. Pulling latest changes...")
        repo = git.Repo(clone_path)
        origin = repo.remotes.origin
        origin.pull()
        #print(f"Updated {clone_path} to latest.")

def ensure_wa_repo():
    ensure_repo("https://github.com/WeakAuras/WeakAuras2.git", "./WeakAuras2")

if __name__ == "__main__":
    ensure_wa_repo()