#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
hugo

# Go To Public folder
cd public
# Add changes to git.
git add --all

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit --message "$msg"

# Push source and build repos.
git push --force origin master

# Come Back
cd ..

# Add changes to git.
git add --all

# Commit changes.
git commit --message "$msg"

# Push source and build repos.
git push --force origin master
