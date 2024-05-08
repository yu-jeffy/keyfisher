import json
import requests
import base64
from tqdm import tqdm
import os
import re
import sys


def list_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)

    repos_info = []  # List to store repo information

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            # Create a dictionary with name and git_url and add it to the list
            repo_info = {"name": repo.get("name"), "git_url": repo.get("git_url")}
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
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"Bearer {token}",
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_sensitive_files(username, repo, token):
    # Load sensitive file names from sensitive_files.json
    with open('sensitive_files.json', 'r') as json_file:
        data = json.load(json_file)
        files_list = data['files']

    # A dictionary to hold the result
    found_files = {}

    # Loop through each file in the files list and try to fetch its contents
    for file_path in tqdm(files_list, file=sys.stdout, desc="Scanning files"):
        file_content = get_file(username, repo, file_path, token)
        if file_content:
            # If content was returned, store the result
            found_files[file_path] = file_content
        else:
            # Instead of printing, you might want to log the missed files quietly
            pass

    return found_files


def skim_files_for_keyword(directory, keyword):
    """
    Skims through files in a specified directory for a given keyword.

    :param directory: The directory containing files to be skimmed.
    :param keyword: The keyword to search for in the files.
    """
    # Walk through all files in the specified directory
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            with open(file_path, "r") as file:
                content = file.read()
                # Check if keyword is in file content
                if keyword.lower() in content.lower():
                    print(f"Keyword found in {file_path}")
                else:
                    print(f"Keyword not found in {file_path}")


def save_fetched_files(username, repo, token):
    # Define a local directory to store the fetched files
    local_dir = f"fetched_files/{username}/{repo}"
    os.makedirs(local_dir, exist_ok=True)

    # Load sensitive file names from sensitive_files.json
    with open("sensitive_files.json", "r") as json_file:
        data = json.load(json_file)
        files_list = data["files"]

    # Loop through each file in the files list and try to fetch its content
    for file_path in files_list:
        file_content = get_file(username, repo, file_path, token)
        if file_content:
            # Define a local file path (assuming file_path doesn't contain directories)
            local_file_path = os.path.join(local_dir, os.path.basename(file_path))
            # Save the file content locally
            with open(local_file_path, "w") as file:
                file.write(file_content)
            # print(f"Saved {file_path} to {local_file_path}")


# skimming for private keys
def skim_files_for_private_keys(directory):
    """
    Skims through files in a specified directory for patterns that may indicate exposed private keys.

    :param directory: The directory containing files to be skimmed.
    """
    # Patterns that match common private key structures
    key_patterns = {
        "SSH Private Key": r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
        "PEM Private Key": r"-----BEGIN PRIVATE KEY-----",
        "AWS API Key": r"(AKIA[0-9A-Z]{16})",
        "AWS Secret Key": r"([0-9a-zA-Z/+]{40})",
        "Azure Storage Key": r"DefaultEndpointsProtocol=https;AccountName=[a-zA-Z0-9]+;AccountKey=[a-zA-Z0-9+/=]+;EndpointSuffix=core\.windows\.net",
        "Google Cloud API Key": r"AIza[0-9A-Za-z\\-_]{35}",
        "Google OAuth Access Token": r"ya29\.[0-9A-Za-z\-_]+",
        "Generic API Key": r"[a-zA-Z0-9]{32,45}",
        "Generic Secret": r"[a-zA-Z0-9]{32,45}",
        "Heroku API Key": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        "Basic Auth Credentials": r"Authorization: Basic [a-zA-Z0-9=]+",
        "FTP Credentials": r"ftp:\/\/[a-zA-Z0-9]+:[a-zA-Z0-9]+@",
        "Database Connection String": r"jdbc:mysql:\/\/[^\s]+",
        "Slack Token": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
        "GitHub Token": r"[a-f0-9]{40}",
        "Mailgun API Key": r"key-[0-9a-zA-Z]{32}",
        "Stripe API Key": r"sk_live_[0-9a-zA-Z]{24}",
        "Private RSA Key Block": r"---+BEGIN.+PRIVATE KEY---+",
        "Twilio API Key": r"SK[0-9a-fA-F]{32}",
        "OpenAI API Key": r"(sk-|pk-)[0-9a-zA-Z]{32}",
        "Discord Bot Token": r"[MN][0-9A-Za-z\\-_]{23}\.[0-9A-Za-z\\-_]{6}\.[0-9A-Za-z\\-_]{27}",
        "LinkedIn Client ID": r"[0-9a-z]{12}",
        "LinkedIn Client Secret": r"[0-9a-zA-Z]{16}",
        "Mailchimp API Key": r"[0-9a-f]{32}-us[0-9]{1,2}",
        "PagerDuty Integration Key": r"[A-Z0-9]{20,32}",
        "Dropbox API Key": r"[a-z2-7]{15}",
        "Dropbox Secret Key": r"[a-z2-7]{15}",
        "Jwt Token": r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-\._\+\/=]*",
        "Asymmetric Private Key": r"-----BEGIN( EC|RSA|DSA)? PRIVATE KEY-----",
    }

    # Walk through all files in the specified directory
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                found_keys = []
                for key_type, pattern in key_patterns.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        found_keys.extend([(key_type, match) for match in matches])

                if found_keys:
                    dir_name, file_name = os.path.split(file_path)
                    last_folder = os.path.basename(dir_name)
                    for key_type, match in found_keys:
                        print(
                            f"Key found, {os.path.join(last_folder, file_name)} is vulnerable. Potential {key_type} found, match: {match}."
                        )
