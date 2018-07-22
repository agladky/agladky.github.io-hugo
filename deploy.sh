#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi

# Calculate css.
cd dev
make
cd ..

# Build the project.
hugo

cd public/ru
git add --all
git commit --message "$msg"
git push --force origin master

cd ..

cd en
git add --all
git commit --message "$msg"
git push --force origin master

cd ../..

git add --all
git commit --message "$msg"
git push --force origin master
