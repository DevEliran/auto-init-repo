cd $1 
git init
git add -A
git commit -m "initial commit"
git branch -M master
git remote add origin git@github.com:$2/$3.git
git push -u origin master
