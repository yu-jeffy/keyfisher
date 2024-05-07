import os
from dotenv import load_dotenv
from scrape import *

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
github_token = os.getenv('GITHUB_TOKEN')

print(list_repos("yu-jeffy", github_token))

print(get_sensitive_files("yu-jeffy", "OnePulse", github_token))