from github import Github
import git
import os
import shutil
import re
import json
from dotenv import load_dotenv
load_dotenv()

import sys
import sys

# Config
FORCE_CLONE = False

# GitHub API Token
GITHUB_API_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

# Initialize GitHub client
g = Github(GITHUB_API_TOKEN)

# Directory to clone repositories
CLONE_DIR = "./cloned_repos"

# Boilerplate pattern (This can be customized based on known patterns)
boilerplate_patterns = [
    r'\/\*\*?.*\*\/',   # Match C-style comments
    r'^import .+',       # Match import statements in Python, JS, etc.
    r'^#include .+',     # Match include statements in C/C++
    r'^package .+',      # Match package statements in Java
    r'^using .+',        # Match using statements in C#
    r'^module .+',       # Match module statements in various languages
]

def clone_repo(repo_url):
    repo_name = repo_url.split('/')[-1]
    repo_dir = os.path.join(CLONE_DIR, repo_name)
    if os.path.exists(repo_dir):
        if FORCE_CLONE:
            # Remove existing directory
            shutil.rmtree(repo_dir)
        else:
            return repo_dir
    git.Repo.clone_from(repo_url, repo_dir)
    return repo_dir

def count_lines(repo_dir: str, file_types : list[str] =['.py', '.js', '.java', '.c', '.cpp', '.cs', '.ts', '.html', '.css',
                                    '.sh', '.go', '.rs', '.php', '.svelte', '.md', '.txt', '.css', '.sh',
                                    '.sql', '.md', '.txt'], ignore_patterns : list[str]=None):
    loc_data = {
        "total_files": 0,
        "total_lines": 0,
        "total_blanks": 0,
        "total_comments": 0,
        "total_lines_of_code": 0,
        "boilerplate_lines": 0,
        "actual_code_lines": 0,
        "language_distribution": {}
    }
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_patterns and any(re.match(pattern, file_path) for pattern in ignore_patterns):
                continue
            if file_path.endswith(tuple(file_types)):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                loc_data["total_files"] += 1
                loc_data["total_lines"] += len(lines)
                for line in lines:
                    if line.strip() == "":
                        loc_data["total_blanks"] += 1
                    elif re.match(r'^\s*#|//|/\*|\*/|<!--', line.strip()):
                        loc_data["total_comments"] += 1
                    else:
                        loc_data["total_lines_of_code"] += 1
                        if any(re.match(pattern, line.strip()) for pattern in boilerplate_patterns):
                            loc_data["boilerplate_lines"] += 1
                        else:
                            loc_data["actual_code_lines"] += 1

                file_extension = os.path.splitext(file_path)[1]
                if file_extension not in loc_data["language_distribution"]:
                    loc_data["language_distribution"][file_extension] = 0
                loc_data["language_distribution"][file_extension] += len(lines)

    return loc_data

def get_repo_languages(repo_dir, ignore_patterns=None):
    languages = set()
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_patterns and any(re.match(pattern, file_path) for pattern in ignore_patterns):
                continue
            file_extension = os.path.splitext(file_path)[1]
            languages.add(file_extension)
    return languages

def analyze_repos(repos, file_types):
    results = {}
    for repo_info in repos:
        repo_path = repo_info["path"]
        repo_name = repo_path.split('/')[-1]
        print(f"Processing {repo_name}...")
        repo_dir = clone_repo("https://github.com/" + repo_path + ".git")
        ignore_patterns = repo_info.get("ignore")
        loc_data = count_lines(repo_dir, file_types, ignore_patterns)
        results[repo_name] = loc_data
    return results

def get_unique_languages(repos):
    unique_languages = set()
    for repo_info in repos:
        repo_path = repo_info["path"]
        repo_dir = clone_repo("https://github.com/" + repo_path + ".git")
        ignore_patterns = repo_info.get("ignore")
        languages = get_repo_languages(repo_dir, ignore_patterns)
        unique_languages.update(languages)
    return unique_languages

def save_results(data, filename="loc_analysis.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)