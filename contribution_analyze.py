import git
import os
from datetime import datetime
import statistics

def get_author_contributions(repo_name: str, author: list[str]):
    # Path to the cloned repo
    repo_path = f"./cloned_repos/{repo_name}"
    
    # Check if the repo exists
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repository {repo_name} not found in /cloned_repos.")
    
    # Initialize the Repo object
    repo = git.Repo(repo_path)
    
    # Ensure the repo is not bare
    if repo.bare:
        raise ValueError(f"Repository {repo_name} is bare.")
    
    # Filter commits by the author
    commits = list(repo.iter_commits(author=author))
    
    # Calculate total number of commits
    total_commits = len(commits)
    
    # Initialize variables for calculating lines added, deleted, and commit dates
    total_additions = 0
    total_deletions = 0
    commit_sizes = []
    commit_dates = []
    
    for commit in commits:
        # Getting the diff data for each commit
        diff_data = commit.stats.total
        additions = diff_data['insertions']
        deletions = diff_data['deletions']
        
        total_additions += additions
        total_deletions += deletions
        commit_sizes.append(additions + deletions)
        commit_dates.append(datetime.fromtimestamp(commit.committed_date))
    
    # Calculate first and last commit dates
    first_commit_date = min(commit_dates) if commit_dates else None
    last_commit_date = max(commit_dates) if commit_dates else None
    
    # Calculate median commit size
    median_commit_size = statistics.median(commit_sizes) if commit_sizes else 0

    # Results
    insights = {
        "total_commits": total_commits,
        "total_lines_changed": {
            "additions": total_additions,
            "deletions": total_deletions
        },
        "first_commit_date": first_commit_date.strftime("%Y-%m-%d %H:%M:%S") if first_commit_date else None,
        "last_commit_date": last_commit_date.strftime("%Y-%m-%d %H:%M:%S") if last_commit_date else None,
        "median_commit_size": median_commit_size
    }
    
    return insights