import os
import shutil
from git import Repo, GitCommandError

WASLIBS_REMOTE = "git@github.com:WAStudios/WASLibs.git"
WASLIBS_REPO_PATH = "./WASLibs"
LOCAL_LIBS_DIR = "./libs"

def clone_or_update_waslibs():
    if not os.path.exists(WASLIBS_REPO_PATH):
        print(f"Cloning WASLibs from {WASLIBS_REMOTE}...")
        Repo.clone_from(WASLIBS_REMOTE, WASLIBS_REPO_PATH)
    else:
        print(f"Updating existing WASLibs repo...")
        try:
            repo = Repo(WASLIBS_REPO_PATH)
            origin = repo.remotes.origin
            origin.pull()
        except GitCommandError as e:
            print(f"Error updating WASLibs: {e}")

def sync_libs_from_waslibs():
    waslibs_libs_dir = os.path.join(WASLIBS_REPO_PATH, "libs")
    if not os.path.exists(waslibs_libs_dir):
        print(f"Error: {waslibs_libs_dir} not found!")
        return

    if os.path.exists(LOCAL_LIBS_DIR):
        print(f"Removing existing {LOCAL_LIBS_DIR}...")
        shutil.rmtree(LOCAL_LIBS_DIR)

    print(f"Copying libraries from WASLibs to {LOCAL_LIBS_DIR}...")
    shutil.copytree(waslibs_libs_dir, LOCAL_LIBS_DIR)
    print("Libraries synced successfully.")

def getlibs():
    clone_or_update_waslibs()
    sync_libs_from_waslibs()