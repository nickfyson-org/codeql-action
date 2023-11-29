import os, json

with open(os.environ["GITHUB_OUTPUT"], "a") as f:

    f.write(f"release_branch=releases/{os.environ['MAJOR_VERSION']}\n")

    # TODO determine the set of older release branches 👆
    # ensure backport_target_branches is empty for anything other than the latest release branch
    # abort if the
    f.write("backport_target_branches="+json.dumps(["releases/v2"])+"\n")
