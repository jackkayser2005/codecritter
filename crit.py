#grab the environment variables first 
import os, requests, json, sys
import urllib.request 
from unidiff import PatchSet
token = os.getenv("GITHUB_TOKEN") # this is injected by actions 
repo = os.getenv("GITHUB_REPOSITORY") # onwwe/reposname

ref = os.getenv("GITHUB_REF")

pr_number = ref.split('/')[2] #so this splits the ref iE refs/pull/42/merge inti [refs, pull,  42, merge]
#then getting the second value of that array returns the PR number which we can use later 

repo_owner = repo.split('/')[0] 
repo_repo = repo.split('/')[1]

url = f"https://api.github.com/repos/{repo_owner}/{repo_repo}/pulls/{pr_number}/files?per_page=100"

#create the url based on the info we have grabbed 

headers = {
    "Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"
}

print("DEBUG: token Length", len(token) if token else "None") #quick check 

#created the auth header 
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()#this will throw an errors 



files = response.json() 



header = f"--- a/{filename}\n+++ b/{filename}\n"
for file in files:
    filename = file["filename"] 
    raw_patch = file["patch"] # we are reconstructing a kind of header so we do not get yelled at 
    header = f"--- a/{filename}\n+++ b/{filename}\n"
    full_patch = header + raw_patch
    if file['patch'] == None or file['additions'] == 0:
        continue # if this is the case we have nothing to parse 
    patch = PatchSet(full_patch)
    added_lines = []
    for patched_file in patch:
        for hunk in patched_file:
            for line in hunk: 
                if line.is_added:
                    added_lines.append(line.value)
    print(file['filename'], len(added_lines), "added lines")


