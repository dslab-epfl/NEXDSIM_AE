## Artifact Evaluation for paper "Fast End-to-End Performance Simulation of Accelerated Hardware-Software Stacks"

Following the guideline, you will be able to run experiments covering three accelerators VTA, Protoacc, JPEG with 4 different simulation modes, NEX+DSim, NEX+RTL, Gem5+DSim and Gem5+RTL.


1. Step 0, clone the repo
```bash
git clone https://github.com/dslab-epfl/NEXDSIM_AE.git
git submodule update --init --recursive
```

2. Step 1, enter container
We provide a Docker container since there are many repositories with a lot of specific dependencies involved. You can either enter the provided VS Code Dev Container (follow [this guide](https://code.visualstudio.com/docs/devcontainers/containers)) or enter the container manually:  
```bash
docker run -v $(pwd):/workspaces/NEXDSIM_AE/ --device=/dev/kvm --privileged -it kaufijonas/nexdsim:sosp25_ae /bin/bash -c "sudo chmod 666 /dev/kvm && /bin/bash"
```

3. Step 2, make SimBricks
Depending on your machine, this step may take up to an hour.
```
cd submodules/simbricks
make -j`nproc`
make -j`nproc` sims/external/gem5/ready
make -j`nproc` sims/external/qemu/ready
make -j`nproc` build-images
make -C sims/external/vta/simbricks
make -C sims/external/protoacc/simbricks
make sims/misc/jpeg_decoder/jpeg_decoder_verilator
```

4. Step 3, run gem5 based experiments
TODO(Jiacheng): This needs the necessary commands

enter `sudo su`
5. Ste 4, make nex. At `make menuconfig` step;
in `Round Based Simulation Options`, enter the configs as mentioned in `submodules/nex/readme.md`. 
install `scx` as mentioned in `submodules/nex/readme.md`.

```bash
cd submodules/nex
```

Outside of nix-shell, do `sudo make scx -j` (because scx won't work with wrapped compiler in nix)

```bash
make menuconfig
make autoconfig
cd experiments
./update_configs_for_all_exp.sh
./build_tvm.sh
./run_all.sh
```


