#!/usr/bin/env python3
import subprocess
import sys
import os

UPSTREAM_URL = "https://github.com"
SHIMS_DIR = "macos27_shims"

def run_git_cmd(args, fail_message):
    """Executes a git command and prints tracking diagnostics."""
    print(f"[*] Running: git {' '.join(args)}")
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] Error: {fail_message}")
        print(f"Details:\n{result.stderr.strip()}")
        return False, result.stderr
    return True, result.stdout.strip()

def check_git_status():
    """Ensures workspace is completely clean before attempting an upstream sync."""
    _, stdout = run_git_cmd(["status", "--porcelain"], "Failed to check repository status.")
    if stdout:
        print("[-] Error: Your working directory contains uncommitted changes.")
        print("Please commit or stash your work before running the sync pipeline.")
        sys.exit(1)

def setup_upstream_remote():
    """Verifies or dynamically provisions the upstream tracking pointer."""
    success, remotes = run_git_cmd(["remote"], "Failed to query existing git remotes.")
    if not success:
        sys.exit(1)
        
    if "upstream" not in remotes.splitlines():
        print("[*] Upstream remote target missing. Configuring tracking link...")
        success, _ = run_git_cmd(["remote", "add", "upstream", UPSTREAM_URL], "Failed to add upstream remote link.")
        if not success:
            sys.exit(1)
        print("[+] Upstream remote registered successfully.")
    else:
        print("[+] Upstream tracking remote found.")

def sync_and_rebase():
    """Fetches updates and rebases your custom development branch."""
    print("[*] Fetching structural modifications from NullMoth core project...")
    success, _ = run_git_cmd(["fetch", "upstream"], "Could not pull updates from upstream metadata servers.")
    if not success:
        sys.exit(1)

    # Determine if upstream has updated main, v3, or golden-gate branches yet
    # Adjust target string below to 'upstream/v3' or 'upstream/golden-gate' when they drop
    target_upstream_branch = "upstream/main"

    print(f"[*] Attempting to rebase your 8 custom commits onto {target_upstream_branch}...")
    rebase_success, _ = run_git_cmd(["rebase", target_upstream_branch], "Rebase encountered severe code structural conflicts.")
    
    if not rebase_success:
        print("\n[!] CRITICAL: Rebase stopped due to conflicting files.")
        print("[*] Because your changes are safely localized inside your patchers directory,")
        print("    you can resolve individual line mismatches manually, then run:")
        print("    'git rebase --continue'")
        sys.exit(1)
        
    print("[+] Rebase finished successfully! Your macOS 27 patches are now layered over the latest code.")

if __name__ == "__main__":
    if not os.path.exists(".git"):
        print("[-] Error: This script must be executed directly from the root of your git workspace.")
        sys.exit(1)
        
    check_git_status()
    setup_upstream_remote()
    sync_and_rebase()
