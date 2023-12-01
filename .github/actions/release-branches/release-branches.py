import argparse
import os, json
import subprocess

# Name of the remote
ORIGIN = 'origin'

OLDEST_SUPPORTED_MAJOR_VERSION = 2

# Runs git with the given args and returns the stdout.
# Raises an error if git does not exit successfully (unless passed
# allow_non_zero_exit_code=True).
def run_git(*args, allow_non_zero_exit_code=False):
  cmd = ['git', *args]
  p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if not allow_non_zero_exit_code and p.returncode != 0:
    raise Exception(f'Call to {" ".join(cmd)} exited with code {p.returncode} stderr: {p.stderr.decode("ascii")}.')
  return p.stdout.decode('ascii')

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--major-version", required=True, type=str, help="The major version of the release")
  parser.add_argument("--latest-tag", required=True, type=str, help="The most recent tag published to the repository")
  args = parser.parse_args()

  major_version = args.major_version
  latest_tag = args.latest_tag

  print("major_version: " + major_version)
  print("latest_tag: " + latest_tag)

  with open(os.environ["GITHUB_OUTPUT"], "a") as f:

    f.write(f"backport_source_branch=releases/{major_version}\n")

    backport_target_branches = []
    major_version_number = int(major_version.strip("v"))

    for i in range(major_version_number-1, 0, -1):
      branch_name = f"releases/v{i}"
      if i >= OLDEST_SUPPORTED_MAJOR_VERSION:
        backport_target_branches.append(branch_name)

    # TODO need to return empty array if the major version is not the latest
    # in order to ensure that the backport job is not triggered
    f.write("backport_target_branches="+json.dumps(backport_target_branches)+"\n")

if __name__ == "__main__":
  main()
