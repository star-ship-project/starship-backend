# STAR S.H.I.P. Contribution Guidelines

Please follow this **Feature Branch Workflow**. This would ensure that the `main` branch always contains working code for our demo.

---

## 1. Sync Your Local Machine
Before starting any new work, always make sure your local `main` branch is up to date with the cloud version.

```bash
git checkout main
git pull origin main
```
## 2. Create a Feature Branch
Never work directly on `main`. Create a **descriptive** branch for every specific task.

```bash
# Format: name/task-description
git checkout -b <your-name>/<task-description>

# Example:
git checkout -b aviles/add-validation-logic
```
## 3. Code and Commit
Work on your changes locally. 

### Commit Message Formats

| Prefix | Use Case | Example |
| :--- | :--- | :--- |
| **feat:** | A new feature or logic change | `feat: add Gemini 2.0 Flash integration` |
| **fix:** | A bug fix | `fix: correct the DepEd ID regex pattern` |
| **docs:** | Documentation only (README, etc.) | `docs: add contribution guidelines` |
| **refactor:** | Code cleanup (no new features/fixes) | `refactor: simplify the process_sms function` |
| **chore:** | Maintenance (requirements, gitignore) | `chore: cleanup requirements.txt` |

<br>

```bash
git add .
git commit -m "feat: descriptive message of what you changed"
```

## 4. After pushing:
- Go to the GitHub repository.
- Click the "Compare & pull request" button.
- Assign another teammate as a Reviewer.


## 5. Review and Merge
1. The designated reviewer will check for errors or suggest improvements.
2. Once approved, use "Squash and merge" to combine your commits into a single clean entry on main.
3. Delete the feature branch from GitHub after the merge is complete.
