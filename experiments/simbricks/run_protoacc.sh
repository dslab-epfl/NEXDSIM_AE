#make -C .. clean
#make -C .. -j

# make -C $HOME/SimBricks-LPN/sims/misc/protoacc/simbricks


tmux new-session -d -s "bench0-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench0" --force ./test_protoacc.py "
tmux new-session -d -s "bench1-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench1" --force ./test_protoacc.py "
tmux new-session -d -s "bench2-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench2" --force ./test_protoacc.py "
tmux new-session -d -s "bench3-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench3" --force ./test_protoacc.py "
tmux new-session -d -s "bench4-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench4" --force ./test_protoacc.py "
tmux new-session -d -s "bench5-rtl" "simbricks-run --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench5" --force ./test_protoacc.py "

tmux new-session -d -s "bench0-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench0" --force ./test_protoacc.py "
tmux new-session -d -s "bench1-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench1" --force ./test_protoacc.py "
tmux new-session -d -s "bench2-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench2" --force ./test_protoacc.py "
tmux new-session -d -s "bench3-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench3" --force ./test_protoacc.py "
tmux new-session -d -s "bench4-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench4" --force ./test_protoacc.py "
tmux new-session -d -s "bench5-lpn" "simbricks-run --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench5" --force ./test_protoacc.py "

# tmux new-session -d -s "bench0-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench0" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench1-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench1" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench2-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench2" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench3-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench3" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench4-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench4" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench5-rtl" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-rtl-gem5_o3-bench5" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "bench0-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench0" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench1-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench1" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench2-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench2" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench3-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench3" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench4-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench4" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "bench5-lpn" "cd $HOME/SimBricks-LPN/experiments && python3 run.py --verbose --force --filter="protoacc_benchmark-lpn-gem5_o3-bench5" --force pyexps/test_protoacc.py --repo $HOME/SimBricks-LPN/"

