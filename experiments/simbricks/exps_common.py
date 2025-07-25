import os

dir_project_root = os.getenv("DIR_PROJECT_ROOT")
dir_simbricks = os.getenv("DIR_SIMBRICKS")
if dir_project_root is None or dir_simbricks is None:
    raise Exception("Some necessary environment variables are not set. Make sure direnv is set up and loads .envrc")