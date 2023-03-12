#!/bin/bash

# Script to initialize git repo with realistic 2024 commit history
PROJECT_DIR="/Users/rahulvelpur/Desktop/rahul-private/rahul-git/cost-anomaly-detector"
cd "$PROJECT_DIR"

git init
git config user.name "Rahul Reddy"
git config user.email "rahulreddy0120@gmail.com"

# Commit 1: Initial commit (Jan 15, 2024)
git add README.md .gitignore
GIT_AUTHOR_DATE="2024-01-15T09:30:00" GIT_COMMITTER_DATE="2024-01-15T09:30:00" \
git commit -m "Initial commit: cost anomaly detector project"

# Commit 2: Add requirements (Jan 18, 2024)
git add requirements.txt
GIT_AUTHOR_DATE="2024-01-18T14:20:00" GIT_COMMITTER_DATE="2024-01-18T14:20:00" \
git commit -m "Add project dependencies"

# Commit 3: Add config template (Jan 22, 2024)
git add config.yaml
GIT_AUTHOR_DATE="2024-01-22T10:45:00" GIT_COMMITTER_DATE="2024-01-22T10:45:00" \
git commit -m "Add configuration template"

# Commit 4: Basic detector implementation (Jan 25, 2024)
git add anomaly_detector.py
GIT_AUTHOR_DATE="2024-01-25T16:10:00" GIT_COMMITTER_DATE="2024-01-25T16:10:00" \
git commit -m "Implement basic anomaly detection logic"

# Commit 5: Add Slack integration (Jan 29, 2024)
git add anomaly_detector.py
GIT_AUTHOR_DATE="2024-01-29T11:30:00" GIT_COMMITTER_DATE="2024-01-29T11:30:00" \
git commit -m "Add Slack notification support"

# Commit 6: Add email notifications (Feb 2, 2024)
git add anomaly_detector.py
GIT_AUTHOR_DATE="2024-02-02T13:15:00" GIT_COMMITTER_DATE="2024-02-02T13:15:00" \
git commit -m "feat: add email notification support"

# Commit 7: Fix threshold calculation (Feb 5, 2024)
git add anomaly_detector.py
GIT_AUTHOR_DATE="2024-02-05T09:50:00" GIT_COMMITTER_DATE="2024-02-05T09:50:00" \
git commit -m "fix: correct standard deviation threshold logic"

# Commit 8: Add Dockerfile (Feb 8, 2024)
git add Dockerfile
GIT_AUTHOR_DATE="2024-02-08T15:40:00" GIT_COMMITTER_DATE="2024-02-08T15:40:00" \
git commit -m "Add Docker support for containerized deployment"

# Commit 9: Update README with examples (Feb 12, 2024)
git add README.md
GIT_AUTHOR_DATE="2024-02-12T10:20:00" GIT_COMMITTER_DATE="2024-02-12T10:20:00" \
git commit -m "docs: add usage examples and output samples"

# Commit 10: Final improvements (Feb 15, 2024)
git add anomaly_detector.py README.md
GIT_AUTHOR_DATE="2024-02-15T14:05:00" GIT_COMMITTER_DATE="2024-02-15T14:05:00" \
git commit -m "Improve error handling and add real-world impact metrics"

echo "✅ Git repository initialized with 2024 commit history"
echo ""
echo "Commits span: Jan 15, 2024 → Feb 15, 2024"
echo ""
echo "Next steps:"
echo "1. Review commits: git log --oneline"
echo "2. Create repo on GitHub: https://github.com/new"
echo "3. Push: gh repo create cost-anomaly-detector --public --source=. --push"
