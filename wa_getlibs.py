import os
import subprocess
import yaml

def valid_refs(target_path):
    """Returns a list of valid remote refs (branches and tags)."""
    result = subprocess.run(
        ["git", "-C", target_path, "ls-remote", "--heads", "--tags", "origin"], capture_output=True, text=True, check=True
    )
    refs = [line.split()[1].replace('refs/heads/', '').replace('refs/tags/', '') for line in result.stdout.splitlines()]
    return refs

def getlibs():
    pkgmeta_path = "./WeakAuras2/.pkgmeta"
    libs_dir = "./libs"

    if not os.path.exists(pkgmeta_path):
        print(f".pkgmeta not found at {pkgmeta_path}")
        return

    with open(pkgmeta_path, "r") as f:
        pkgmeta_data = yaml.safe_load(f)

    externals = pkgmeta_data.get("externals", {})
    print(f"Starting library sync from .pkgmeta...")

    if not os.path.exists(libs_dir):
        os.makedirs(libs_dir, exist_ok=True)
        print(f"Created new libs directory: {libs_dir}")
    else:
        print(f"Using existing libs directory: {libs_dir}")

    print(f"Found {len(externals)} externals in .pkgmeta")

    for path, data in externals.items():
        target_path = os.path.join(libs_dir, os.path.basename(path))
        if isinstance(data, str):
            url = data
            branch_or_tag = None
        elif isinstance(data, dict):
            url = data.get("url")
            branch_or_tag = data.get("tag") or data.get("commit")
        else:
            print(f"Unknown format for {path}, skipping.")
            continue

        if os.path.exists(target_path):
            if os.path.exists(os.path.join(target_path, ".git")):
                print(f"Updating existing git repo {url} in {target_path}...")

                try:
                    # Fetch latest refs
                    refs = valid_refs(target_path)

                    # Check if the repo is on a branch or detached HEAD
                    result = subprocess.run(["git", "-C", target_path, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)
                    current_branch = result.stdout.strip()

                    if current_branch == "HEAD":
                        print(f"{target_path} is in a detached HEAD state, resetting...")
                        subprocess.run(["git", "-C", target_path, "fetch"], check=True)

                        if branch_or_tag in refs:
                            subprocess.run(["git", "-C", target_path, "checkout", branch_or_tag], check=True)
                        else:
                            fallback = "master" if "master" in refs else "main"
                            subprocess.run(["git", "-C", target_path, "reset", "--hard", f"origin/{fallback}"], check=True)
                            subprocess.run(["git", "-C", target_path, "checkout", fallback], check=True)
                    else:
                        print(f"Pulling latest changes on branch {current_branch} for {target_path}...")
                        subprocess.run(["git", "-C", target_path, "pull"], check=True)

                except subprocess.CalledProcessError as e:
                    print(f"Git operation failed for {target_path}: {e}")
                continue
            elif os.path.exists(os.path.join(target_path, ".svn")):
                print(f"Updating existing svn repo {url} in {target_path}...")
                subprocess.run(["svn", "update", target_path], check=True)
                continue

        if "townlong-yak.com" in url or url.endswith(".git") or "github.com" in url:
            print(f"Cloning git repo {url} into {target_path}...")
            git_clone_cmd = ["git", "clone", url, target_path]
            subprocess.run(git_clone_cmd, check=True)
            if branch_or_tag:
                print(f"Checking out {branch_or_tag} in {target_path}...")
                subprocess.run(["git", "-C", target_path, "checkout", branch_or_tag], check=True)
        else:
            print(f"Checking out svn repo {url} into {target_path}...")
            subprocess.run(["svn", "checkout", url, target_path], check=True)

    print("All libraries fetched or updated successfully.")
