#grab the environment variables first 
import os, requests, json, sys

token = os.getenv("GITHUB_TOKEN") # this is injected by actions 
repo = os.getenv("GITHUB_REPOSITORY") # onwwe/reposname
print(repo)
ref = os.getenv("GITHUB_REF")

pr_number = ref.split('/')[2] #so this splits the ref iE refs/pull/42/merge inti [refs, pull,  42, merge]
#then getting the second value of that array returns the PR number which we can use later 

repo_owner = repo.split('/')[0] 
repo_repo = repo.split('/')[1]

url = f"https://api.github.com/repos/{repo_owner}/{repo_repo}/pulls/{pr_number}/files?per_page=100"

#create the url based on the info we have grabbed 

header = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
#created the auth header 
response = requests.get(url, headers=header, timeout=30)
response.raise_for_status()#this will throw an errors 



files = response.json() 

for f in files:
    print(" *", f["filename"])


