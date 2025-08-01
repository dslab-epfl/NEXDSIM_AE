#!/bin/bash

SESSION="run_protoacc"

tmux new-session -d -s "$SESSION" 

tmux new-window -t "$SESSION" -n "bench0-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench0 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench1-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench1 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench2-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench2 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench3-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench3 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench4-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench4 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench5-rtl" "simbricks-run --verbose --force --filter=protoacc_benchmark-rtl-gem5_o3-bench5 --force ./test_protoacc.py; bash"

tmux new-window -t "$SESSION" -n "bench0-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench0 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench1-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench1 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench2-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench2 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench3-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench3 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench4-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench4 --force ./test_protoacc.py; bash"
tmux new-window -t "$SESSION" -n "bench5-lpn" "simbricks-run --verbose --force --filter=protoacc_benchmark-lpn-gem5_o3-bench5 --force ./test_protoacc.py; bash"

# Attach to the session
tmux attach-session -t "$SESSION"
