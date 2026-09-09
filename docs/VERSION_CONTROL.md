# Git and GitHub workflow

## Local checkpoints

The repository starts on `main` with one clean initial commit. Review changes before each later commit:

```bash
git status
git diff
git add -- assignments/A01-topic/README.md assignments/A01-topic/work/main.py
git diff --cached
git commit -m "Complete A01 baseline"
```

Replace the example paths with files that exist. Do not force-add ignored files casually. Instructor materials, raw data, original prompts, generated output, virtual environments, IDE state, and secrets remain outside ordinary commits. Source code, report sources, selected submissions, and metadata are eligible for tracking.

Ignored files are not backed up by Git or GitHub. Retain a separate permitted backup or a documented download source for course materials and datasets.

## Publish later

Use one separate private GitHub repository for this course. Review instructor restrictions before uploading any course-provided content; a private repository does not itself grant redistribution permission. This local setup creates no remote and uploads nothing.

After creating an empty private GitHub repository with the same course code, inspect tracked files and connect it explicitly:

```bash
git status
git ls-files
git remote add origin https://github.com/YOUR-ACCOUNT/COURSE-CODE.git
git remote -v
git push -u origin main
```

If `origin` already exists by then, inspect its URL before changing it. Pull before beginning work that may have changed on another computer.
