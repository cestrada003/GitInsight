import requests
import pandas as pd


# Function to retrieve open Pull Requests from a repository using the GitHub API token
def get_repo_data(repo_url, token):
    """
    Retrieves data for a given repository.
    """
    headers = {"Authorization": f"token {token}"}
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle repository not found error
        return None


def get_open_pull_requests(repo, token):
    """
    Retrieves open pull requests for a non-archived repository.
    """
    repo_url = f"https://api.github.com/repos/{repo}"
    pull_requests_url = f"https://api.github.com/repos/{repo}/pulls?state=open"

    repo_data = get_repo_data(repo_url, token)
    if not repo_data:
        # Handle repository not found error
        return []

    if not repo_data["archived"]:
        headers = {"Authorization": f"token {token}"}
        response = requests.get(pull_requests_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Extract desired data
            pull_requests = []
            for pull_request in data:
                try:
                    if not pull_request["draft"]:
                        pull_requests.append({
                            "created_at": pull_request["created_at"],
                            "user": pull_request["user"]["login"],
                            "html_url": pull_request["html_url"],
                        })
                except Exception as e:
                    # Handle error
                    print(f"Error occurred for repo '{repo}': {e}")
                    continue
            return pull_requests

        else:
            # Handle error retrieving pull requests
            return []
    else:
        return []


# Path to file containing list of repositories
repos_file = "repos.txt"

# Path to file containing the token
token_file = "token.txt"

# Read the token from the file
with open(token_file, "r") as f:
    token = f.read().strip()

# # GitHub API token
# token = "test"

# Read repositories from file
repos = []
with open(repos_file, "r") as f:
    for line in f:
        repo = line.strip()
        if repo:
            repos.append(repo)

# Retrieve open Pull Requests from each repository
pull_requests = []
for repo in repos:
    if repo.startswith("--"):
        # Skip repos starting with "--"
        continue
    pull_requests.extend(get_open_pull_requests(repo, token))

# Create a DataFrame from the pull requests data
df = pd.DataFrame(pull_requests, columns=["created_at", "user", "html_url"])

# Convert "created_at" to datetime and extract date in "YYYY-MM-DD" format
df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

# Sort the data by the "created_at" column in descending order
df = df.sort_values(by="created_at", ascending=True)

# Output the sorted data to an Excel file
df.to_excel("open_pull_requests.xlsx", index=False)

print("Open Pull Requests retrieved and saved to open_pull_requests.xlsx")
