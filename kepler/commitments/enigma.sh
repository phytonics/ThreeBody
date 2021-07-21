# First, we check status for the sake of checking all grounds
git status

# Next, we add the actual files to the blob
git add notebooks/*8462852*.ipynb

# Next, of course, we must commit
git commit -m "Update KIC 8462852 Analysis"

# We now push it to origin
git push origin

# We shall check the status again just in case
git status
