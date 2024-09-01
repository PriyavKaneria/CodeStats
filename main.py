import json
import os
import sys
from clone_and_analyze import analyze_repos, get_unique_languages, save_results
from visualize import visualize_data

def main():
    # Get the list of repositories to analyze from repos.json
    repos = []
    with open("repos.json") as f:
        repos = json.load(f)

    analyze_file_types = ['.jsx', '.rb', '.mdx', '.rs', '.json', '.xml', '.js', '.less',
                           '.scss', '.md', '.go', '.elm', '.pyw', '.ts', '.yaml', '.toml',
                             '.html', '.tsx', '.properties', '.py', '.php', '.kt', '.pug', 
                             '.yml', '.cjs', '.heex', '.svelte', '.txt', '.css', '.ex']

    # get arguments and analyze or get data accordingly
    if len(sys.argv) > 1:
        if sys.argv[1] == "analyze":
            analysis = analyze_repos(repos, analyze_file_types)
            save_results(analysis)
            return
        elif sys.argv[1] == "languages":
            languages = get_unique_languages(repos)
            print(languages)
            return
        elif sys.argv[1] == "visualize":
            if not os.path.exists("loc_analysis.json"):
                print("Run analysis first to generate data.")
                return
            with open("loc_analysis.json") as f:
                data = json.load(f)
            visualize_data(data)
            return
    else:
        print("Auto-analyzing repositories...")
        analysis = analyze_repos(repos, analyze_file_types)
        save_results(analysis)
        visualize_data(analysis)

if __name__ == "__main__":
    main()