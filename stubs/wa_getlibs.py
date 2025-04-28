import os
import shutil
import stat
import time
from git import Repo

WASLIBS_REMOTE = "git@github.com:WAStudios/WASLibs.git"
WASLIBS_TEMP_DIR = "./WASLibs_TEMP"
LOCAL_LIBS_DIR = "./WeakAuras2/WeakAuras/Libs"

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except PermissionError:
        print(f"Retrying deletion for locked file: {path}")
        time.sleep(0.5)
        try:
            func(path)
        except Exception as e:
            print(f"Failed to delete {path}: {e}")
            raise

def clone_and_extract_libs():
    # Clean up any old temp WASLibs directory
    if os.path.exists(WASLIBS_TEMP_DIR):
        print(f"Removing existing {WASLIBS_TEMP_DIR}...")
        shutil.rmtree(WASLIBS_TEMP_DIR, onerror=handle_remove_readonly)

    # Clone WASLibs repo into temp dir
    print(f"Cloning WASLibs into {WASLIBS_TEMP_DIR}...")
    Repo.clone_from(WASLIBS_REMOTE, WASLIBS_TEMP_DIR)

    # Clean ./libs directory
    if os.path.exists(LOCAL_LIBS_DIR):
        print(f"Removing existing {LOCAL_LIBS_DIR}...")
        shutil.rmtree(LOCAL_LIBS_DIR, onerror=handle_remove_readonly)

    # Copy all contents of WASLibs_TEMP into LOCAL_LIBS_DIR
    print(f"Copying libraries from {WASLIBS_TEMP_DIR} to {LOCAL_LIBS_DIR}...")
    shutil.copytree(WASLIBS_TEMP_DIR, LOCAL_LIBS_DIR)

    # Remove the temp WASLibs clone entirely
    print(f"Removing temporary {WASLIBS_TEMP_DIR} directory...")
    shutil.rmtree(WASLIBS_TEMP_DIR, onerror=handle_remove_readonly)

    print("Libraries are ready in ./WeakAuras2/WeakAuras/Libs and cleanup is complete.")

def getlibs():
    clone_and_extract_libs()
