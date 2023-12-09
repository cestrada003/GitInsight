## GitHub Pull Request Fetcher

This repository contains code to retrieve open pull requests from a list of GitHub repositories using the GitHub API.

### Features

* Retrieves data for non-archived repositories.
* Filters for open and non-draft pull requests.
* Extracts desired data: creation date, user, and pull request URL.
* Saves extracted data to an Excel file.

### Requirements

* Python 3.6+
* `requests` library
* `pandas` library
* List of repositories in a file named `repos.txt` (one repository per line)
* GitHub API token in a file named `token.txt`

### Usage

1. Install the required libraries:

```bash
pip install requests pandas
```

2. Add your list of repositories to `repos.txt`.
3. Add your GitHub API token to `token.txt`.
4. Run the script:

```bash
python pull_request_fetcher.py
```

5. Open the `open_pull_requests.xlsx` file to view the extracted data.

### Output

An Excel file named `open_pull_requests.xlsx` containing the following columns:

* **created_at:** Date the pull request was created (YYYY-MM-DD)
* **user:** Username of the pull request author
* **html_url:** URL of the pull request on GitHub

This script can be helpful for automating the process of collecting information about open pull requests for a set of repositories.
