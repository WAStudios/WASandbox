import os
import shutil
import stat
import time
from git import Repo

WASLIBS_REMOTE = "git@github.com:WAStudios/WASLibs.git"
WASLIBS_TEMP_DIR = "./WASLibs_TEMP"
LOCAL_LIBS_DIR = "./libs"

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

    # WASLibs/libs/ contains what we need
    waslibs_libs_dir = os.path.join(WASLIBS_TEMP_DIR, "libs")

    # Clean ./libs directory
    if os.path.exists(LOCAL_LIBS_DIR):
        print(f"Removing existing {LOCAL_LIBS_DIR}...")
        shutil.rmtree(LOCAL_LIBS_DIR, onerror=handle_remove_readonly)

    # Copy only the contents of WASLibs/libs into ./libs/
    print(f"Copying libraries from {waslibs_libs_dir} to {LOCAL_LIBS_DIR}...")
    shutil.copytree(waslibs_libs_dir, LOCAL_LIBS_DIR)

    # Remove the temp WASLibs clone entirely
    print(f"Removing temporary {WASLIBS_TEMP_DIR} directory...")
    shutil.rmtree(WASLIBS_TEMP_DIR, onerror=handle_remove_readonly)

    # Ensure no lingering WASLibs folder
    if os.path.exists("./WASLibs"):
        print("Removing leftover ./WASLibs folder...")
        shutil.rmtree("./WASLibs", onerror=handle_remove_readonly)

    print("Libraries are ready in ./libs and cleanup is complete.")

def getlibs():
    clone_and_extract_libs()
