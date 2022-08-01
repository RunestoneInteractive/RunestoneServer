set -e

if [ $# -eq 0 ]
  then
    echo "Usage:  makeRelease <release no>"
    exit
fi

while true; do
read -p "Did you update/commit the version in pyproject.toml " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

 
echo "tagging this release and pushing to github"

git tag -a $1 -m 'tag new version'
git push --follow-tags
