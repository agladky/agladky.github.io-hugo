#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi

echo -e "\033[0;32mPull sites...\033[0m"
rm -rf public/
mkdir public
cd public
git clone git@github.com:agladky/agladky.github.io.git ru
git clone git@github.com:agladky/agladky.com.git en
cd ..

echo -e "\033[0;32mCalculate css...\033[0m"
cd dev
make
cd ..

echo -e "\033[0;32mBuild new version...\033[0m"
hugo

echo -e "\033[0;32mPush ru version...\033[0m"
cd public/ru
git add --all
git commit --message "$msg"
git push --force origin master
cd ../..

echo -e "\033[0;32mPush en version...\033[0m"
cd public/ru
git add --all
git commit --message "$msg"
git push --force origin master
cd ../..

echo -e "\033[0;32mPush hugo code...\033[0m"
git add --all
git commit --message "$msg"
git push --force origin master
