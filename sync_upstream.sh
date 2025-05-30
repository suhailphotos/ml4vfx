#!/usr/bin/env bash
set -e

# 0) one-time in your main ml4vfx repo:
git remote get-url upstream >/dev/null 2>&1 || \
  git remote add upstream https://github.com/pixelknit/rebelwayAppliedML.git
git fetch upstream

# 1) map your local branch names → instructor’s branch names
declare -A upstreamMap=(
  [data3D]=3d_data
  [api]=api
  [compBasics]=computer_basics
  [vision]=computer-vision
  [dataIO]=experiment/dataio
  [experiments]=experiments
  [houdini]=houdini
  [nlp]=nlp
  [reinforce]=reinforcement
  [sklearn]=scikitlearn
  [tensorFlow]=tensorflow
)

# 2) for each worktree, pull the correct upstream branch
git worktree list --porcelain \
  | awk '/^worktree /{print $2}' \
  | while read -r WT; do
      echo
      echo "⟶ Entering: $WT"
      cd "$WT"

      branch=$(git rev-parse --abbrev-ref HEAD)
      echo "   local branch: $branch"

      # look up upstream branch (fall back to same name)
      upstreamBranch=${upstreamMap[$branch]:-$branch}

      # only pull if that remote branch exists
      if git show-ref --verify --quiet "refs/remotes/upstream/$upstreamBranch"; then
        echo "   pulling upstream/$upstreamBranch → $branch"
        git pull --ff-only upstream "$upstreamBranch"
      else
        echo "   skipping (no upstream/$upstreamBranch)"
      fi
    done

echo && echo "✅ all done."
