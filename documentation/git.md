# Tagg
https://www.atlassian.com/git/tutorials/inspecting-a-repository/git-tag

create a new tag for a release 
git tag -a v0.1 -m "first tag"
push the tag 
git push origin v1.1

link release with tag

<!-- Remove local branches that are merged into master -->
git branch --merged master | grep -v '^[ *]*master$' | xargs git branch -d
<!-- Prune remote -->
git remote prune origin