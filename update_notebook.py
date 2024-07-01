import requests
from getpass import getpass
import json
import base64
import os

def get_file_sha(repo_owner, repo_name, file_path_in_repo, token, branch):
    """Get the SHA of the file from the GitHub repository."""
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}?ref={branch}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    return response_data['sha']

def update_file_on_github(repo_owner, repo_name, file_path_in_repo, content, token, file_sha, branch):
    """Update the file content on GitHub."""
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}'
    headers = {'Authorization': f'token {token}'}
    update_data = {
        'message': 'Update notebook with latest changes',
        'content': base64.b64encode(content.encode()).decode(),
        'sha': file_sha,
        'branch': branch
    }
    response = requests.put(url, headers=headers, data=json.dumps(update_data))
    return response

def main():
    # GitHub repository details
    repo_owner = 'ratulb'  # Replace with your GitHub username
    repo_name = 'pytorch'  # Replace with your GitHub repository name
    file_path_in_repo = 'chap_1_from_scratch.ipynb'  # Replace with the path to your notebook in the repo
    branch = 'main'  # Use the appropriate branch name

    # Get your GitHub personal access token (PAT) securely
    token = getpass('Enter your GitHub personal access token: ')

    # Save the current notebook to a local file
    notebook_filename = 'current_notebook.ipynb'
    os.system('jupyter nbconvert --to notebook --output {} --output-dir . {}'.format(notebook_filename, notebook_filename))

    # Read the content of your notebook
    with open(notebook_filename, 'r') as file:
        content = file.read()

    # Get the file SHA
    file_sha = get_file_sha(repo_owner, repo_name, file_path_in_repo, token, branch)

    # Update the file on GitHub
    response = update_file_on_github(repo_owner, repo_name, file_path_in_repo, content, token, file_sha, branch)

    if response.status_code == 200:
        print('Notebook updated successfully on GitHub.')
    else:
        print(f'Failed to update notebook: {response.status_code}')
        print(response.json())

if __name__ == '__main__':
    main()

