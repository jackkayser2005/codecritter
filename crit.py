#grab the environment variables first 
import os, requests, json, sys
import urllib.request 
from unidiff import PatchSet
token = os.getenv("GITHUB_TOKEN") # this is injected by actions 
repo = os.getenv("GITHUB_REPOSITORY") # onwwe/reposname

openai_key = os.getenv("OPENAI_API_KEY")
ref = os.getenv("GITHUB_REF")
if not openai_key:
    print("No OPENAI_API_KEY provided; No access to AI models")
else:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)

pr_number = ref.split('/')[2] #so this splits the ref iE refs/pull/42/merge inti [refs, pull,  42, merge]
#then getting the second value of that array returns the PR number which we can use later 
repo_owner = repo.split('/')[0] 
repo_repo = repo.split('/')[1]

url = f"https://api.github.com/repos/{repo_owner}/{repo_repo}/pulls/{pr_number}/files?per_page=100"

#create the url based on the info we have grabbed 

headers = {
    "Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"
}



#created the auth header 
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()#this will throw an errors 



files = response.json() 




for file in files:
    raw_patch = file.get("patch")
    if raw_patch == None or file['additions'] == 0:
         continue  #this will now be changed to skip any binary huge or anything with no changes 
    filename = file['filename'] 
     # we are reconstructing a kind of header so we do not get yelled at 
    header = f"--- a/{filename}\n+++ b/{filename}\n" #disgusting behavior on this 
    full_patch = header + raw_patch
    patch = PatchSet(full_patch)
    added_lines = []
    for patched_file in patch:
        for hunk in patched_file:
            for line in hunk: 
                if line.is_added:
                    added_lines.append(line.value)
   # print(file['filename'], len(added_lines), "changed lines")
    if openai_key and added_lines:
        prompt = (
            "You are CodeCritter, an automated pull request reviewer. \n"
            f"File: {filename}\n"
            "New lines added (truncated):\n"
            + "\n".join(added_lines[:100])[:3500] +
            "\n---\nGive three concise suggestions (<=120 words)\n"
            "If changes look great a simple perfect. will do, \n"
            "if issues with code arise give pointers to lines that need help\n"
            "You are able to detect bugs and fix issues as a senior developer would\n"
            "you are to be a helpful assistant and aid the user in any way possible."
        )
        response = client.chat.completions.create(
            model='gpt-4.1-nano',
            temperature=0.3,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        feedback = response.choices[0].message.content.strip() 
        print(f"\n AI feedback for {filename}:\n{feedback}\n")
    else:
        print(f"Skipped {filename} (no added Lines or no API key)")