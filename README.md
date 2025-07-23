# CodeCritter

AI-powered pull-request reviewer for GitHub.

## What it does
* Parses the diff of every PR
* Sends added lines to GPT-4.1-nano
* Posts a single **CodeCritter review** comment with 3 bullet suggestions per file

## Usage
1. Copy `.github/workflows/codecritter.yml` into your repo  
2. Add two secrets  
   * `GITHUB_TOKEN` (auto-generated)  
   * `OPENAI_API_KEY`  
3. Merge a PR – CodeCritter will comment automatically.

## Config
| ENV | Default | Description |
|-----|---------|-------------|
| `OPENAI_MODEL` | `gpt-4.1-nano` | Change to `gpt-3.5-turbo`, etc. |
| `MAX_LINES` | 100 | Truncate large diffs |

## Roadmap
* Inline diff comments  
* ESLint/Radon integration  
* Cached feedback to skip unchanged files

## 🛡️  Permissions & Fork Behaviour

| Scenario | What happens | Why |
|----------|--------------|-----|
| **PR from a branch in the *same* repo** | CodeCritter posts a single `### CodeCritter review` comment. | Workflow’s `issues: write` permission + repo’s *Read & write* token are available. |
| **PR from a fork** | Comment is **not** posted. Feedback is still visible in **Actions → Logs**. | GitHub supplies a **read-only** token to workflows triggered by forked PRs. Attempting to write would 403. |

### Enabling comments on fork PRs (optional)

1. **Repo Settings → Actions → General → Workflow permissions**  
   Set to **Read & write**.  
2. Replace the fork-guard or add a writable token:  
   * Use a second workflow that triggers on `pull_request_target`, **or**  
   * Provide a fine-grained PAT secret with “Issues: write” scope.

If you prefer the safer default, keep the guard as-is; reviewers can still read CodeCritter’s suggestions in the Action log.

## License
MIT – see LICENSE file.
