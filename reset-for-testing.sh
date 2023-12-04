
set -e

TARGET_REPO="nickfyson-org/codeql-action"

SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_PATH=$(echo "$SCRIPT_PATH" | sed 's/^.\///')
git clean -fdx -e $SCRIPT_PATH
git reset --hard -e $SCRIPT_PATH

# pull all tags from nickfyson-org/codeql-action and prune any that have been deleted
git fetch --tags --prune-tags

# get SHA of main on github/codeql-action
main_sha=$(gh api /repos/github/codeql-action/commits/main --jq '.sha')

# get SHA of tag v1 on github/codeql-action
v2_sha=$(gh api /repos/github/codeql-action/commits/v2 --jq '.sha')

# reset local main to match github/codeql-action
git checkout main
git fetch origin main
git reset --hard $main_sha
git push -f origin main

# reset local v2 to match github/codeql-action
git checkout v2
git reset --hard $v2_sha
git tag -f v2
git push -f origin v2

git checkout main

latest_tag=$(gh api /repos/github/codeql-action/tags --jq '.[].name' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)

return_later() {
    echo "$1\n$2" | sort -V | tail -n 1
}

# iterate over all the remote tags using the gh api which match the semver pattern or v1, v2, v3 etc
for tag in $(gh api /repos/$TARGET_REPO/tags --jq '.[].name' | grep -E '^v[0-9]+(?:\.[0-9]+\.[0-9]+$)?'); do

    # compare semver of tag to latest_tag and delete it from the remote if it is newer
    if [[ $(return_later "$tag" "$latest_tag") == "$tag" ]]; then
        if [[ "$tag" == "$latest_tag" ]]; then
            continue
        else
            echo "DELETING $tag as it is newer than $latest_tag"
            gh api -X DELETE /repos/$TARGET_REPO/git/refs/tags/$tag
        fi
    fi
done

# apply the patch of an upstream PR the local checkout
gh api repos/github/codeql-action/pulls/2014 -H "Accept: application/vnd.github.patch" | git apply

# ensure that the automation workflows are enabled to run on this fork repo
if [[ "$OSTYPE" == "darwin"* ]]; then
    find .github -type f -exec sed -i '' 's/github\/codeql-action/nickfyson-org\/codeql-action/g' {} \;
else
    find .github -type f -exec sed -i 's/github\/codeql-action/nickfyson-org\/codeql-action/g' {} \;
fi
