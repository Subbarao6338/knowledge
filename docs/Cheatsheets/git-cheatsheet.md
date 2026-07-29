---
layout: default
title: "Git Cheatsheet"
---

# Git Cheatsheet

## The Four Areas of Git

Before the commands, it helps to know **where** your code lives at any moment:

1. **Working Directory** — where you actually edit files (untracked or modified).
2. **Staging Area (Index)** — a prep zone where you organize what goes into your next commit.
3. **Local Repository** — your committed history on your machine (the `.git` folder).
4. **Remote Repository** — the hosted version on GitHub, GitLab, Bitbucket, etc.

Most Git commands move content between these four areas.

---

## 1. Setup & Config

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "vim"       # or "code --wait", "nano", etc.
git config --global color.ui auto            # colored terminal output
git config --list                            # show all config
git config --global alias.st status          # create an alias

# Advanced Config Details
git config --global core.autocrlf input      # (Mac/Linux) LF on commit, LF on disk
git config --global core.autocrlf true       # (Windows) LF on commit, CRLF on disk
git config --global pull.rebase true         # automatically rebase on pull
git config --global rerere.enabled true      # reuse recorded resolution of conflicts
```

---

## 2. Starting a Repository

```bash
git init                                     # new repo in current dir
git clone <url>                              # clone existing repo
git clone <url> <folder-name>                # clone into specific folder
git clone -b <branch> --single-branch <url>  # clone only one branch
git clone --depth 1 <url>                    # shallow clone (latest commit only)
```

---

## 3. The Daily Workflow (Basic Snapshotting)

```bash
git status                        # what's changed
git status -s                     # short format
git diff                          # unstaged changes vs last commit

git add <file>                    # stage a file
git add .                         # stage everything in current dir
git add -p                        # stage interactively, hunk by hunk

git commit -m "message"           # commit staged changes
git commit -am "message"          # stage tracked files + commit (skips new files)
git commit --amend                # edit the last commit
git commit --amend --no-edit      # add staged changes to last commit, same message
```

---

## 4. Viewing History

```bash
git log                           # full history
git log --oneline                 # condensed
git log --oneline --graph --all   # visual branch graph
git log -p                        # show diffs per commit
git log -p <file>                 # diffs for a specific file over time
git log -n 5                      # last 5 commits
git log --author="name"           # filter by author
git log --since="2 weeks ago"     # filter by date
git log -- <file>                 # history of a specific file
git log --stat                    # show file change stats per commit
git show <commit>                 # show a specific commit's changes
git blame <file>                  # who changed each line, and when
```

---

## 5. Diffing

```bash
git diff                                # unstaged changes vs last commit
git diff --staged                       # staged changes vs last commit
git diff <branch1> <branch2>            # compare two branches
git diff HEAD~1 HEAD                    # compare last two commits
git diff <commit1> <commit2> -- <file>  # diff a file between commits
```

---

## 6. Branching

```bash
git branch                        # list local branches (current has *)
git branch -a                     # list all branches (local + remote)
git branch <name>                 # create branch
git branch -d <name>               # delete branch (safe, only if merged)
git branch -D <name>               # force delete branch
git branch -m <old> <new>          # rename branch

git switch <name>                  # switch to branch (modern)
git switch -c <name>                # create + switch (modern)
git checkout <name>                 # switch to branch (classic)
git checkout -b <name>               # create + switch (classic)
```

---

## 7. Merging & Rebasing

```bash
git merge <branch>                 # merge branch into current
git merge --no-ff <branch>         # force a merge commit (no fast-forward)
git merge --abort                  # bail out of a conflicted merge

git rebase <branch>                # rebase current branch onto another
git rebase -i HEAD~5                # interactive rebase, last 5 commits
git rebase --continue               # after resolving conflicts
git rebase --abort                  # bail out of a rebase
git rebase --skip                   # skip the current commit during rebase
```

**Interactive rebase commands:** `pick`, `reword`, `edit`, `squash`, `fixup`, `drop`

### Interactive Rebasing Deep-Dive
When you run `git rebase -i HEAD~3`, your editor will display a list of the last 3 commits, prefixed with commands:
```text
pick f7f3f2d feat: add authentication middleware
pick 310aef4 fix: handle null user profiles
pick d041a31 docs: update api documentation
```
- **pick:** Use the commit as is.
- **reword:** Use the commit, but edit the commit message.
- **edit:** Stop during rebasing to edit files (amend the commit).
- **squash:** Melds commit into the previous one, opening editor to combine messages.
- **fixup:** Like squash, but discards this commit's log message.
- **drop:** Remove the commit entirely.

---

## 8. Remotes — Sharing & Syncing

```bash
git remote -v                      # list remotes
git remote add origin <url>        # add a remote
git remote remove origin           # remove a remote
git remote set-url origin <url>    # change remote URL

git fetch                          # download changes, don't merge
git fetch --all                    # fetch all remotes
git pull                           # fetch + merge
git pull --rebase                  # fetch + rebase instead of merge
git push                           # push current branch
git push origin <branch>           # push a specific branch
git push -u origin <branch>        # push + set upstream tracking
git push --force-with-lease        # safer force push (checks remote hasn't changed)
git push origin --delete <branch>  # delete a remote branch
```

### Multi-Remote Workflows
When collaborating across multiple forks or environments, you can configure several remotes:
```bash
git remote add upstream <parent-repo-url> # track original parent repository
git fetch upstream                       # fetch updates from original source
git merge upstream/main                  # merge parent updates into your local main
```

---

## 9. Stashing (Temporary Workspaces)

```bash
git stash                          # stash tracked changes
git stash -u                       # include untracked files
git stash save "message"           # stash with a descriptive name
git stash list                     # list stashes
git stash pop                      # apply + remove most recent stash
git stash apply                    # apply most recent stash, keep it in list
git stash apply stash@{2}          # apply a specific stash
git stash drop stash@{2}           # delete a specific stash
git stash clear                    # delete all stashes
git stash show -p stash@{0}        # view stash contents as a diff
```

---

## 10. Undoing Things (Disaster Recovery)

Git is designed, so almost nothing is permanently lost once it's been committed — see the reflog section below if you think you've lost work.

```bash
# Discard unstaged changes
git restore <file>                 # discard unstaged changes to a file (modern)
git checkout -- <file>             # same, classic syntax

# Unstage a file (keep the changes)
git restore --staged <file>        # modern
git reset <file>                   # classic

# Fix the last commit
git commit --amend -m "corrected message"

# Undo commits (move HEAD back)
git reset --soft HEAD~1            # undo last commit, keep changes staged
git reset --mixed HEAD~1           # undo last commit, keep changes unstaged (default)
git reset --hard HEAD~1            # undo last commit, discard changes entirely
git reset --hard HEAD              # discard ALL local modifications since last commit

# Undo a commit safely on a shared/remote branch (creates a new "anti-commit")
git revert <commit>
git revert -n <commit>             # revert without auto-committing

# Remove untracked files
git clean -n                       # dry run: preview what would be removed
git clean -fd                      # actually remove untracked files and directories
```

---

## 11. Tags

```bash
git tag                            # list tags
git tag v1.0.0                     # lightweight tag on current commit
git tag -a v1.0.0 -m "message"     # annotated tag
git tag -a v1.0.0 <commit>         # tag a specific commit
git push origin v1.0.0             # push a single tag
git push origin --tags             # push all tags
git tag -d v1.0.0                  # delete local tag
git push origin --delete v1.0.0    # delete remote tag
```

---

## 12. Inspecting & Comparing

```bash
git show <commit>:<file>           # view a file as of a specific commit
git ls-files                       # list tracked files
git ls-tree -r HEAD                # list all files in current tree
git shortlog -sn                   # commit count per author
```

---

## 13. Finding Things

```bash
git grep "pattern"                 # search working tree
git log -S "string"                # find commits that added/removed a string
git log -G "regex"                 # find commits matching a regex in diffs
git bisect start                   # start binary search for a bad commit
git bisect bad                     # mark current commit as bad
git bisect good <commit>           # mark a commit as good
git bisect reset                   # end bisect session
```

---

## 14. Submodules

```bash
git submodule add <url> <path>           # add a submodule
git submodule update --init --recursive  # init + fetch submodules after clone
git submodule update --remote            # pull latest for submodules
```

---

## 15. Cherry-Picking

Grab a single commit from a different branch and apply it to your current one:

```bash
git cherry-pick <commit>                 # apply a specific commit to current branch
git cherry-pick <commit1> <commit2>      # apply multiple commits
git cherry-pick --continue               # after resolving conflicts
git cherry-pick --abort                  # bail out
```

---

## 16. Worktrees

```bash
git worktree add ../path <branch>  # check out a branch into a separate folder
git worktree list                  # list active worktrees
git worktree remove <path>         # remove a worktree
```

---

## 17. Reflog — The Safety Net

> If you ever run `git reset --hard` by mistake and think you've lost all your work: don't panic. Git keeps a silent journal of every action you take — even deleted branches or discarded commits are recoverable. Run `git reflog` to find the hash of your work from before the mistake, then restore it.

```bash
git reflog                         # history of HEAD movements
git reset --hard HEAD@{2}          # jump back to a reflog state
git branch <name> <sha>            # recreate a branch at a specific reflog commit
```

---

## 18. Common Workflows

**Undo a bad `git add`:**
```bash
git restore --staged <file>
```

**Fix the last commit message:**
```bash
git commit --amend -m "new message"
```

**Sync a feature branch with main:**
```bash
git switch feature-branch
git fetch origin
git rebase origin/main
```

**Squash last N commits into one:**
```bash
git rebase -i HEAD~N
# mark all but the first as "squash" or "fixup"
```

**Discard all local changes and match remote exactly:**
```bash
git fetch origin
git reset --hard origin/main
```

**Recover a deleted branch:**
```bash
git reflog                         # find the commit SHA
git branch <branch-name> <sha>
```

---

## 19. .gitignore Quick Reference

```
*.log              # ignore all .log files
!important.log      # but not this one
build/               # ignore a directory
/config.local        # ignore only at root level
**/temp               # ignore "temp" anywhere in the tree
```

---

## 20. Commit Message Convention (Conventional Commits)

```
feat: add user login endpoint
fix: correct null pointer in payment flow
docs: update README with setup steps
refactor: simplify auth middleware
test: add coverage for edge cases
chore: bump dependency versions
```

---

## 21. Git Rerere (Reuse Recorded Resolution)

`rerere` is a hidden gem that tells Git to remember how you resolved a hunk conflict, so the next time it sees the same conflict, it can resolve it for you automatically.

```bash
# Enable it globally
git config --global rerere.enabled true

# To see recorded resolutions at any point
git rerere status
git rerere diff
```

This is extremely useful when doing long-running feature branches that require constant rebases onto `main`.

---

## 22. Dual-Remote Branching Setup (Forks & Upstreams)

When working with a forked repository (common in open source), maintain reference to the original parent repository as `upstream` and your fork as `origin`:

```bash
# Add original parent repository
git remote add upstream https://github.com/parent-owner/parent-repo.git

# Verify remotes
git remote -v
# origin   https://github.com/your-username/parent-repo.git (fetch/push)
# upstream https://github.com/parent-owner/parent-repo.git (fetch/push)

# Sync your local main with upstream main
git checkout main
git fetch upstream
git merge upstream/main

# Sync your fork's remote on GitHub
git push origin main

---

## 23. Git Hooks (Automation and Validation)

Git Hooks are scripts that run automatically before or after key Git actions (like commit, push, or receive). They live in the `.git/hooks/` directory of your repository.

### Standard Hooks
- **pre-commit:** Runs before a commit is created. Used to validate code syntax, run tests, or run lint/format checks.
- **prepare-commit-msg:** Runs before the commit message editor opens.
- **commit-msg:** Validates the format of the commit message (e.g. enforcing conventional commits).
- **pre-push:** Runs before files are uploaded to the remote server. Ideal for full integration test checks.

### Example: `.git/hooks/pre-commit` (Bash script)
To make a hook active, create a file named exactly `pre-commit` inside `.git/hooks/`, add your script, and make it executable:

```bash
#!/bin/sh

echo "Running pre-commit hooks..."

# Execute linting suite
npm run lint

# Capture exit code
if [ $? -ne 0 ]; then
    echo "Linter failed. Commit aborted."
    exit 1
fi

echo "All checks passed. Committing changes."
exit 0
```

To make the script executable on Unix systems:
```bash
chmod +x .git/hooks/pre-commit
```

### Managing Hooks in Teams: Husky (Node.js ecosystem)
Since the `.git` directory is not checked into version control, you can use Husky to share hook scripts with team members automatically.

```bash
# Install Husky
npm install husky --save-dev

# Enable Git hooks
npx husky install

# Add a pre-commit check
npx husky add .husky/pre-commit "npm test"
```

---

## 24. Git Large File Storage (LFS)

Git Large File Storage (LFS) replaces large files such as audio clips, videos, datasets, and graphics with text pointers inside Git, while storing the file contents on a remote server like GitHub or GitLab.

### Installation & Initialization
```bash
# Install Git LFS command-line extension
git lfs install
```

### Tracking Large Files
```bash
# Track all .psd or large dataset files
git lfs track "*.psd"
git lfs track "*.zip"

# Ensure the LFS tracking configuration is committed
git add .gitattributes
git commit -m "chore: track psd and zip files via git lfs"
```

### Inspection & Status
```bash
# List all tracked paths
git lfs track

# List all files currently being tracked in LFS in the active commit
git lfs ls-files
```

---

## 25. Advanced Branch Auditing & Garbage Collection

When working on large repositories over several years, references pile up and the underlying Object Database needs optimization or cleaning.

```bash
# Check database health and find dangling/unreachable objects
git fsck --full --strict

# Run garbage collection, compressing file revisions and removing unreachable objects
git gc --prune=now --aggressive
```
