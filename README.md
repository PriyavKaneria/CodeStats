# CodeStats
A quick project to calculate and analyze stats for all my github, gitlab, local projects

Clones the repositories, counts the lines of code, and calculates the stats.

## Output stats

CLI Visualization
![visualization_screenshot](https://github.com/user-attachments/assets/ee704556-8767-4dbe-baa6-d8b55aeaeb14)

Demo
https://github.com/user-attachments/assets/2040aa75-929c-4267-b392-e32f0e81ea43


`loc_analysis.json`
```json5
    "repo_name": {
        "total_files": "number",
        "total_lines": "number",
        "total_blanks": "number",
        "total_comments": "number",
        "total_lines_of_code": "number",
        "boilerplate_lines": "number", // import statements, require statements, etc for now
        "actual_code_lines": "number",
        "language_distribution": {
            "language_extension": "number_of_lines", // supports any language can be configured as below
        },
        "description": "string",
        "stars": "number", // if repo accessible
        "topics": ["string"], // if repo accessible
        "contributions": {
            "total_commits": "number",
            "total_lines_changed": {
                "additions": "number",
                "deletions": "number",
            },
            "first_commit_date": "datetime_string",
            "last_commit_date": "datetime_string",
            "median_commit_size": "float",
        }
    },
```

## Usage

### Requirements

Recommended Python version: 3.10+
```bash
pip install -r requirements.txt
```

### Configuration

Create a `repos.json` file in the root directory with the following structure:

```json5
[
    {
        "source": "github", // only github supported for now [local, gitlab to be added]
        "path": "REPO_OWNER/REPO_NAME",
        "ignore": ["files", "to", "ignore"],
        "contributor": true // optional, default: false
    },
]
```

### Run

If you have cmake installed, you can use make commands to run the project

#### Getting unique languages across all repos
```bash
make languages
```
OR
```bash
python main.py languages
```

> The languages can be configured in the `main.py` file using the `analyze_file_types` variable

#### Calculating analysis for all repos
```bash
make analyze
```
OR
```bash
python main.py analyze
```

#### Visualizing the stats
```bash
make visualize
```
OR
```bash
python main.py visualize
```
