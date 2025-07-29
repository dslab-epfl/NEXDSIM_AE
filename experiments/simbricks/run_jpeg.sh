
# make -C .. sims/misc/jpeg_decoder/jpeg_decoder_verilator 
cur_dir=$(pwd)
echo "Current directory: $cur_dir"
nix_shell_dir=$cur_dir/../../

mkdir -p log

tmux new-session -d -s "jpeg_rtl_multithreaded_1" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-1' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_rtl_multithreaded_2" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-2' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_rtl_multithreaded_4" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-4' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_rtl_multithreaded_8" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-8' ./jpeg_decoder_multithreaded.py"

tmux new-session -d -s "jpeg_lpn_multithreaded_1" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-1' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_lpn_multithreaded_2" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-2' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_lpn_multithreaded_4" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-4' ./jpeg_decoder_multithreaded.py"
tmux new-session -d -s "jpeg_lpn_multithreaded_8" "simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-8' ./jpeg_decoder_multithreaded.py"

tmux new-session -d -s "jpeg_rtl" "simbricks-run --verbose --force --filter='jpeg_decoder-gem5_o3-rtl' ./jpeg_decoder.py"
tmux new-session -d -s "jpeg_lpn" "simbricks-run --verbose --force --filter='jpeg_decoder-gem5_o3-lpn' ./jpeg_decoder.py"


# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-8' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_8_rtl 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-4' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_4_rtl 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-2' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_2_rtl 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-1' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_1_rtl 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-8' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_8_lpn 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-4' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_4_lpn 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-2' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_2_lpn 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-1' ./jpeg_decoder_multithreaded.py > log/jpeg_multi_1_lpn 2>&1 &

# simbricks-run --verbose --force --filter='jpeg_decoder-gem5_o3-rtl' ./jpeg_decoder.py > log/jpeg_single_1_rtl 2>&1 &
# simbricks-run --verbose --force --filter='jpeg_decoder-gem5_o3-lpn' ./jpeg_decoder.py > log/jpeg_single_1_lpn 2>&1 &

# wait

# tmux new-session -d -s "jpeg_rtl" "python3 run.py --verbose --force --filter='jpeg_decoder-gem5_o3-rtl' --force pyexps/jpeg_decoder.py --repo $HOME/SimBricks-LPN/" 
# tmux new-session -d -s "jpeg_lpn" "python3 run.py --verbose --force --filter='jpeg_decoder-gem5_o3-lpn' --force pyexps/jpeg_decoder.py --repo $HOME/SimBricks-LPN/"  

# tmux new-session -d -s "jpeg_lpn_multithreaded_1" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-1' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"  
# tmux new-session -d -s "jpeg_lpn_multithreaded_2" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-2' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"  
# tmux new-session -d -s "jpeg_lpn_multithreaded_4" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-4' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"  
# tmux new-session -d -s "jpeg_lpn_multithreaded_8" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-lpn-8' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"  

# tmux new-session -d -s "jpeg_rtl_multithreaded_1" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-1' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "jpeg_rtl_multithreaded_2" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-2' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "jpeg_rtl_multithreaded_4" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-4' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "jpeg_rtl_multithreaded_8" "python3 run.py --verbose --force --filter='jpeg_decoder_multithreaded_post-gem5_o3-rtl-8' --force pyexps/jpeg_decoder_multithreaded.py --repo $HOME/SimBricks-LPN/"
