#!/usr/bin/env bash
# Build the lecture notes (in full and chapter by chapter), the standalone background appendix, the per-chapter exercise sheets
# and the private solutions.
# Usage: ./build.sh            (from anywhere; outputs go to lectures/ and exercises/)
set -euo pipefail
cd "$(dirname "$0")"
# Remove every file LaTeX produces except the final PDFs, on success or failure.
# KEEP_AUX=1 ./build.sh keeps the auxiliary files, to inspect the logs.
cleanup() {
  [ -n "${KEEP_AUX:-}" ] && return
  find lectures exercises -path lectures/figures -prune -o -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' \
    -o -name '*.toc' -o -name '*.lof' -o -name '*.lot' -o -name '*.bbl' -o -name '*.blg' \
    -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' -o -name '*.nav' \
    -o -name '*.snm' -o -name '*.idx' -o -name '*.ilg' -o -name '*.ind' -o -name '*.thm' \) \
    -exec rm -f {} +
  rm -f exercises/exercises.pdf
}
trap cleanup EXIT
# run DIR ARGS...: run pdflatex inside DIR.
run() {
  local dir=$1; shift
  if ! (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error "$@" >/dev/null); then
    echo "LaTeX failed in $dir: $*"
    log=$(ls -t "$dir"/*.log | head -1)
    grep -A5 '^!' "$log" || tail -20 "$log"
    exit 1
  fi
}
# Notes and exercises cross-reference each other, so alternate a few passes.
for _ in 1 2 3; do
  run exercises -jobname=exercises exercises.tex
  run lectures -jobname=lecture_notes main.tex
done
# Appendix A as a standalone document, with the numbering of the notes.
for _ in 1 2; do
  run lectures -jobname=background background.tex
done
# The notes chapter by chapter, with the numbering and cross-references of the full notes.
for k in 1 2 3 4 5 6 7 8; do
  for _ in 1 2; do
    run lectures -jobname=chapter$k "\def\chapteronly{$k}\input{main}"
  done
done
# Chapter sheets and their solutions, using the numbering of the combined sheet.
for k in 1 2 3 4 5 6 7 8; do
  name=exercises_chapter$k
  for _ in 1 2; do
    run exercises -jobname=$name "\def\chapteronly{$k}\input{exercises}"
    run exercises -jobname=${name}_solutions "\def\chapteronly{$k}\def\withsolutions{}\input{exercises}"
  done
done
for f in lectures/lecture_notes lectures/chapter{1,2,3,4,5,6,7,8} lectures/background exercises/exercises exercises/exercises_chapter{1,2,3,4,5,6,7,8} exercises/exercises_chapter{1,2,3,4,5,6,7,8}_solutions; do
  n=$(grep -cE "undefined|multiply defined" "$f.log" || true)
  echo "$f.pdf: $(pdfinfo "$f.pdf" | awk '/Pages/{print $2}') pages, $n reference warnings"
done
