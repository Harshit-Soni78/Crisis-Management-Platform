#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update && apt-get install -y git-lfs
git lfs pull
pip install -r requirements.txt