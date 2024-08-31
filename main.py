import requests
import json
import time

def get_loc_data(source, path, ignore=None):
    base_url = "https://api.codetabs.com/v1/loc"
    params = {
        f"{source}": path
    }
    if ignore:
        params["ignored"] = ",".join(ignore)

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {source}/{path}")
        print(response.text)
        return None

def analyze_data(data):
    analysis = {
        "projects": [],
        "overall": {
            "total_files": 0,
            "total_lines": 0,
            "total_blanks": 0,
            "total_comments": 0,
            "total_lines_of_code": 0,
            "language_distribution": {}
        }
    }

    for project_data in data:
        project_analysis = {
            "source": project_data["source"],
            "total_files": 0,
            "total_lines": 0,
            "total_blanks": 0,
            "total_comments": 0,
            "total_lines_of_code": 0,
            "languages": []
        }
        for language_data in project_data["data"]:
            project_analysis["total_files"] += language_data["files"]
            project_analysis["total_lines"] += language_data["lines"]
            project_analysis["total_blanks"] += language_data["blanks"]
            project_analysis["total_comments"] += language_data["comments"]
            project_analysis["total_lines_of_code"] += language_data["linesOfCode"]

            if language_data["language"] != "Total":
                if language_data["language"] not in analysis["overall"]["language_distribution"]:
                    analysis["overall"]["language_distribution"][language_data["language"]] = 0
                analysis["overall"]["language_distribution"][language_data["language"]] += language_data["linesOfCode"]

            project_analysis["languages"].append(language_data)

        analysis["overall"]["total_files"] += project_analysis["total_files"]
        analysis["overall"]["total_lines"] += project_analysis["total_lines"]
        analysis["overall"]["total_blanks"] += project_analysis["total_blanks"]
        analysis["overall"]["total_comments"] += project_analysis["total_comments"]
        analysis["overall"]["total_lines_of_code"] += project_analysis["total_lines_of_code"]

        analysis["projects"].append(project_analysis)

    return analysis

def save_results(data, filename="loc_analysis.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # Get the list of repositories to analyze from repos.json
    repos = []
    with open("repos.json") as f:
        repos = json.load(f)

    collected_data = []
    for repo in repos:
        print(f"Processing {repo['source']}/{repo['path']}")
        loc_data = get_loc_data(repo["source"], repo["path"], repo.get("ignore"))
        if loc_data:
            collected_data.append({
                "source": f"{repo['source']}/{repo['path']}",
                "data": loc_data
            })
        time.sleep(6)

    analysis = analyze_data(collected_data)
    save_results(analysis)

if __name__ == "__main__":
    main()
