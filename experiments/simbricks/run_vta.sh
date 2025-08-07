# make -C .. clean
# make -C .. -j
# make -C ../sims/external/vta/simbricks

# spin up tmux for each one in the following 


# mkdir -p log

tmux new-session -d -s "vtatest-gt-rtl" "simbricks-run --verbose --force --filter='vtatest-gt-rtl' ./vtatest.py"
tmux new-session -d -s "vtatest-gt-lpn" "simbricks-run --verbose --force --filter='vtatest-gt-lpn' ./vtatest.py"

tmux new-session -d -s "classify_resnet18_rtl" "simbricks-run --verbose --force --filter='classify-resnet18_v1-vta-gem5_o3-rtl-4-2000' --force ./classify_simple.py"
tmux new-session -d -s "classify_resnet18_lpn" "simbricks-run --verbose --force --filter='classify-resnet18_v1-vta-gem5_o3-lpn-4-2000' --force ./classify_simple.py"

tmux new-session -d -s "classify_resnet34_rtl" "simbricks-run --verbose --force --filter='classify-resnet34_v1-vta-gem5_o3-rtl-4-2000' --force ./classify_simple.py"
tmux new-session -d -s "classify_resnet34_lpn" "simbricks-run --verbose --force --filter='classify-resnet34_v1-vta-gem5_o3-lpn-4-2000' --force ./classify_simple.py"

tmux new-session -d -s "classify_resnet50_rtl" "simbricks-run --verbose --force --filter='classify-resnet50_v1-vta-gem5_o3-rtl-4-2000' --force ./classify_simple.py"
tmux new-session -d -s "classify_resnet50_lpn" "simbricks-run --verbose --force --filter='classify-resnet50_v1-vta-gem5_o3-lpn-4-2000' --force ./classify_simple.py"

tmux new-session -d -s "detect_rtl" "simbricks-run --verbose --force --filter='detect-vta-gem5_o3-rtl-2000' --force ./detect_simple.py"
tmux new-session -d -s "detect_lpn" "simbricks-run --verbose --force --filter='detect-vta-gem5_o3-lpn-2000' --force ./detect_simple.py"

tmux new-session -d -s "classify_lpn_8" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-lpn-8' --force ./classify_multi.py "

tmux new-session -d -s "classify_rtl_8" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-rtl-8' --force ./classify_multi.py "

tmux new-session -d -s "classify_lpn_4" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-lpn-4' --force ./classify_multi.py "

tmux new-session -d -s "classify_rtl_4" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-rtl-4' --force ./classify_multi.py "


# python3 run.py --verbose --force --filter="classify-resnet18_v1-vta-gem5_o3-rtl-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ & 
# python3 run.py --verbose --force --filter="classify-resnet34_v1-vta-gem5_o3-rtl-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ & 

# python3 run.py --verbose --force --filter="classify-resnet18_v1-vta-gem5_o3-lpn-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ & 
# python3 run.py --verbose --force --filter="classify-resnet34_v1-vta-gem5_o3-lpn-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ & 

# python3 run.py --verbose --force --filter="classify-resnet50_v1-vta-gem5_o3-rtl-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ &
# python3 run.py --verbose --force --filter="classify-resnet50_v1-vta-gem5_o3-lpn-4-2000" --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/ &
# tmux new-session -d -s "classify_resnet50_lpn" "simbricks-run --verbose --force --filter='classify-resnet50_v1-vta-gem5_o3-lpn-4-2000' --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "classify_resnet50_rtl" "simbricks-run --verbose --force --filter='classify-resnet50_v1-vta-gem5_o3-rtl-4-2000' --force pyexps/classify_simple.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "classify_lpn_8" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-lpn-8' --force pyexps/classify_multi.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "classify_rtl_8" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-rtl-8' --force pyexps/classify_multi.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "classify_lpn_4" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-lpn-4' --force pyexps/classify_multi.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "classify_rtl_4" "simbricks-run --verbose --force --filter='classify_multi-resnet18_v1-vta-go3-rtl-4' --force pyexps/classify_multi.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "detect_lpn" "simbricks-run --verbose --force --filter='detect-vta-gem5_o3-lpn-2000' --force pyexps/detect_simple.py --repo $HOME/SimBricks-LPN/"
# tmux new-session -d -s "detect_rtl" "simbricks-run --verbose --force --filter='detect-vta-gem5_o3-rtl-2000' --force pyexps/detect_simple.py --repo $HOME/SimBricks-LPN/"

# tmux new-session -d -s "vtatest-gt-rtl" "simbricks-run --verbose --force --filter='vtatest-gt-rtl' --force experiments/simbricks/vtatest.py"
# tmux new-session -d -s "vtatest-gt-lpn" "simbricks-run --verbose --force --filter='vtatest-gt-lpn' --force experiments/simbricks/vtatest.py"