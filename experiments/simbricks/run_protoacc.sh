#!/bin/bash

SESSION="run_protoacc"
BENCHES=(0 1 2 3 4 5)

tmux new-session -d -s "$SESSION" -n "bench${BENCHES[0]}-rtl" \
  "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench0 --force ./test_protoacc.py; bash"
echo bench${BENCHES[0]}-rtl started

for i in "${BENCHES[@]:1}"; do
  tmux new-window -t "$SESSION" -n "bench$i-rtl" \
    "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench$i --force ./test_protoacc.py; bash"
  echo bench${i}-rtl started
done

for i in "${BENCHES[@]}"; do
  tmux new-window -t "$SESSION" -n "bench$i-lpn" \
    "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench$i --force ./test_protoacc.py; bash"
  echo bench${i}-lpn started
done

# Attach to the session
tmux attach-session -t "$SESSION"
