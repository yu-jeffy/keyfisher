# KeyFisher

KeyFisher is a powerful tool designed to enhance security and compliance by scanning GitHub repositories for exposed sensitive files and keys that could potentially lead to security vulnerabilities. It aims to help developers, DevOps, and security teams identify and remediate these risks promptly.

## Features

- **Repository Scanning**: Efficiently scans all repositories linked to a specified GitHub username for sensitive files.
- **Sensitive File Detection**: Utilizes a comprehensive list (defined in `sensitive_files.json`) of filenames that commonly contain sensitive information, including configuration files, private keys, API tokens, and more.
- **Progress Monitoring**: Implements a loading bar for real-time feedback during the scanning process, improving the usability and monitoring capability of the tool.
- **Content Pattern Matching**: Searches within files for patterns indicative of sensitive information, such as SSH private keys, AWS access keys, Google Cloud tokens, and others, using regular expressions.
- **Result Reporting**: Reports findings in a detailed and structured manner, highlighting potentially vulnerable files and their locations.

## Installation

Before you begin, ensure you have Python 3.6+ installed on your machine. KeyFisher also requires the `requests` and `tqdm` packages, which can be installed using pip:

```sh
pip install requests tqdm
```

### Setup

1. Clone the KeyFisher repository to your local machine using Git:

```sh
git clone https://github.com/your-username/keyfisher.git
cd keyfisher
```

2. Prepare a `.env` file in the root directory of KeyFisher with your GitHub token:

```plaintext
GITHUB_TOKEN=your_github_access_token_here
```

3. Ensure the `sensitive_files.json` file is updated according to your needs. This file should list the filenames which you want to check for sensitive content.

## Usage

To use KeyFisher, run the `main.py` script from the command line, specifying the GitHub username to scan:

```sh
python main.py
```

The script will fetch repositories for the given username, scan for sensitive files, and check their contents for patterns indicative of security risks.

### Custom Configuration

- **Modifying Sensitive Files**: Edit `sensitive_files.json` to adjust which files are scanned.
- **Pattern Adjustments**: Modify the regex patterns in the scanning functions within `scrape.py` as necessary to better fit the specific sensitive information you're concerned about.

## Disclaimer

KeyFisher is developed with the intention of promoting better security practices. It should only be used to scan repositories you own or have explicit permission to analyze. Always adhere to GitHub's API usage policies. The creators of KeyFisher assume no responsibility for misuse of this tool or any potential damages that arise from its use. User discretion is advised, and users are encouraged to follow ethical guidelines and obtain necessary permissions when scanning repositories that are not their own.