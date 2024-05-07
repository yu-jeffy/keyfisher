import requests
import base64
import json

def list_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)
    
    repos_info = []  # List to store repo information
    
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            # Create a dictionary with name and git_url and add it to the list
            repo_info = {
                "name": repo.get("name"),
                "git_url": repo.get("git_url")
            }
            repos_info.append(repo_info)
        return repos_info
    else:
        print(f"Error fetching repos: {response.status_code}")
        return []

def get_file(username, repo, path, token):
    """
    Fetches the contents of a file from a GitHub repository.

    :param username: The username of the owner of the repository.
    :param repo: The name of the repository.
    :param path: The path to the file within the repository.
    :param token: Your GitHub personal access token.
    :return: The contents of the file if successful, None otherwise.
    """
    api_url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        # Decode the file content from base64
        file_content_base64 = response.json()['content']
        file_content = base64.b64decode(file_content_base64).decode('utf-8')
        return file_content
    else:
        print(f"Error fetching file contents: {response.status_code}")
        return None

def get_sensitive_files(username, repo, token):
    # Load sensitive file names from sensitive_files.json
    with open('sensitive_files.json', 'r') as json_file:
        data = json.load(json_file)
        files_list = data['files']

    # A dictionary to hold the result
    found_files = {}

    # Loop through each file in the files list and try to fetch its contents
    for file_path in files_list:
        file_content = get_file(username, repo, file_path, token)
        if file_content:
            # If content was returned, store the result
            found_files[file_path] = file_content
        else:
            print(f"File not found or access denied: {file_path}")

    return found_files