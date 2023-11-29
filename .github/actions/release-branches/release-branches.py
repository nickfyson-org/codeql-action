import argparse
import os, json

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--major-version", required=True, type=str, help="The major version of the release")
  args = parser.parse_args()

  major_version = args.major_version

  print(f"major-version::{major_version}")

  with open(os.environ["GITHUB_OUTPUT"], "a") as f:

    f.write(f"release_branch=releases/{major_version}\n")

    # TODO determine the set of older release branches 👆
    # ensure backport_target_branches is empty for anything other than the latest release branch
    # abort if the
    f.write("backport_target_branches="+json.dumps(["releases/v2"])+"\n")
