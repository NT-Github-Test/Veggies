import os
import shutil
import subprocess
from pathlib import Path

def run_git_command(command, folder_path, error_message):
    """
    Executes a git command in the specified folder
    """
    try:
        result = subprocess.run(
            command,
            cwd=folder_path,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Success: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error {error_message}: {e.stderr.strip()}")
        return False

def init_and_push_to_git(folder_path, folder_name, github_base_url):
    """
    Initializes a git repository with main and feature branches
    """
    print(f"\nInitializing git repository for {folder_name}...")
    
    # Initialize git repository
    if not run_git_command(
        "git init",
        folder_path,
        "initializing git repository"
    ):
        return False

    # Create and checkout main branch first
    if not run_git_command(
        "git checkout -b main",
        folder_path,
        "creating main branch"
    ):
        return False

    # Add all files
    if not run_git_command(
        "git add .",
        folder_path,
        "adding files to git"
    ):
        return False

    # Create initial commit
    if not run_git_command(
        'git commit -m "Initial commit"',
        folder_path,
        "creating initial commit"
    ):
        return False

    # Add remote origin
    remote_url = f"{github_base_url}/{folder_name}.git"
    if not run_git_command(
        f"git remote add origin {remote_url}",
        folder_path,
        "adding remote origin"
    ):
        return False

    # Push main branch
    if not run_git_command(
        "git push -u origin main",
        folder_path,
        "pushing main branch"
    ):
        return False

    # Create and checkout feature branch
    branch_name = f"feature/{folder_name.lower()}"
    if not run_git_command(
        f"git checkout -b {branch_name}",
        folder_path,
        f"creating branch {branch_name}"
    ):
        return False

    # Push feature branch
    if not run_git_command(
        f"git push -u origin {branch_name}",
        folder_path,
        "pushing feature branch"
    ):
        return False

    print(f"Successfully initialized and pushed {folder_name} to GitHub")
    return True

def duplicate_folder_structure(source_folder, target_names, github_base_url):
    """
    Duplicates a folder structure and initializes git repositories for new folders only
    """
    parent_dir = str(Path(source_folder).parent)
    
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder '{source_folder}' does not exist!")
    
    print(f"\nSkipping git initialization for existing folder: {source_folder}")
    
    # Create and initialize duplicates
    for target_name in target_names:
        target_path = os.path.join(parent_dir, target_name)
        
        if os.path.exists(target_path):
            print(f"Warning: Target folder '{target_path}' already exists. Removing it...")
            shutil.rmtree(target_path)
        
        try:
            # Copy the folder structure (excluding .git directory)
            def ignore_git(dir, files):
                return ['.git']
            
            shutil.copytree(source_folder, target_path, ignore=ignore_git)
            print(f"Successfully created duplicate: {target_path}")
            
            # Initialize git for the new folder
            init_and_push_to_git(target_path, target_name, github_base_url)
            
        except Exception as e:
            print(f"Error processing {target_path}: {str(e)}")

def print_folder_structure(path, level=0):
    """
    Prints the folder structure in a tree-like format
    """
    indent = "  " * level
    print(f"{indent}{os.path.basename(path)}/")
    
    try:
        for item in os.listdir(path):
            if item == '.git':  # Skip .git directory
                continue
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print_folder_structure(item_path, level + 1)
            else:
                print(f"{indent}  {item}")
    except Exception as e:
        print(f"Error accessing {path}: {str(e)}")

if __name__ == "__main__":
    # Configuration
    source_folder = "./Veggies"
    target_names = ["Verduras", "Gemuse", "Groenten"]
    github_base_url = "git@github.com:NT-Github-Test"
    
    try:
        # Duplicate folders and initialize git
        duplicate_folder_structure(source_folder, target_names, github_base_url)
        
        # Print the resulting structure
        print("\nCreated folder structures:")
        print_folder_structure(source_folder)
        for target in target_names:
            print_folder_structure(os.path.join(os.path.dirname(source_folder), target))
            
    except Exception as e:
        print(f"An error occurred: {e}")
