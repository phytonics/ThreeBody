# First let's check the status
git status

# We now add the file as in the arguments
for i in $(seq 2 $#);
    do git add ${!i};
done

# Commit files based on first argument
git commit -m "$1"

# Push repo to origin
git push origin

# Check status again
git status
