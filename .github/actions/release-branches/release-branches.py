import argparse
import os, json
import subprocess

# Name of the remote
ORIGIN = 'origin'

# Runs git with the given args and returns the stdout.
# Raises an error if git does not exit successfully (unless passed
# allow_non_zero_exit_code=True).
def run_git(*args, allow_non_zero_exit_code=False):
  cmd = ['git', *args]
  p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if not allow_non_zero_exit_code and p.returncode != 0:
    raise Exception(f'Call to {" ".join(cmd)} exited with code {p.returncode} stderr: {p.stderr.decode("ascii")}.')
  return p.stdout.decode('ascii')

# Returns true if the given branch exists on the origin remote
def branch_exists_on_remote(branch_name):
  return run_git('ls-remote', '--heads', ORIGIN, branch_name).strip() != ''

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--major-version", required=True, type=str, help="The major version of the release")
  parser.add_argument("--latest-tag", required=True, type=str, help="The most recent tag published to the repository")
  args = parser.parse_args()

  major_version = args.major_version
  latest_tag = args.latest_tag

  print("major_version: " + major_version)
  print("latest_tag: " + latest_tag)
  print("REF: " + os.environ["GITHUB_REF"])

  with open(os.environ["GITHUB_OUTPUT"], "a") as f:

    f.write(f"backport_source_branch=releases/{major_version}\n")

    backport_target_branches = []
    major_version_number = int(major_version.strip("v"))

    for i in range(major_version_number-1, 0, -1):
      print(i)
      branch_name = f"releases/v{i}"
      if branch_exists_on_remote(branch_name):
        backport_target_branches.append(branch_name)
    f.write("backport_target_branches="+json.dumps(backport_target_branches)+"\n")

if __name__ == "__main__":
  main()
