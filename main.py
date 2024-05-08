import os
from dotenv import load_dotenv
from scrape import *

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
github_token = os.getenv("GITHUB_TOKEN")


def main(username, token):
    """
    Orchestrates the fetching of repositories, saving sensitive files, and processing them.

    :param username: GitHub username to fetch repositories from.
    :param token: Personal Access Token for GitHub.
    :param keyword: Keyword to search within the fetched files.
    """
    # Get a list of repositories
    repos_info = list_repos(username, token)

    if not repos_info:
        print("No repositories found or there was an error fetching the repositories.")
        return
    
    print()
    
    for repo_info in tqdm(repos_info, desc="Scanning files"):
        
        print()
        
        repo_name = repo_info["name"]
        tqdm.write(f"Processing repository: {repo_name}")

        # Save sensitive files from the repository
        save_fetched_files(username, repo_name, token)

        # Assuming files are saved in a known directory structure
        files_directory = f"fetched_files/{username}/{repo_name}"

        # Skim files for the keyword
        skim_files_for_private_keys(files_directory)

        tqdm.write(f"Finished processing repository: {repo_name}")


# Replace the placeholders with actual values before running
USERNAME = "yu-jeffy"
TOKEN = github_token

if __name__ == "__main__":
    main(USERNAME, TOKEN)
