## Artifact Evaluation for paper "Fast End-to-End Performance Simulation of Accelerated Hardware-Software Stacks"

Following this guide, you will be able to run experiments covering three accelerators VTA, Protoacc, JPEG with 4 different simulation modes, NEX+DSim, NEX+RTL, gem5+DSim and gem5+RTL.


### Step 0: Clone the Repo
```bash
git clone https://github.com/dslab-epfl/NEXDSIM_AE.git
git submodule update --init --recursive
```

### Step 1: Enter Container
We provide a Docker container since there are many repositories with a lot of specific dependencies involved. You can either enter the provided VS Code Dev Container (follow [this guide](https://code.visualstudio.com/docs/devcontainers/containers)) or enter the container manually:  
```bash
docker run -v $(pwd):/NEXDSIM_AE/ --device=/dev/kvm --privileged -it kaufijonas/nexdsim:sosp25_ae /bin/bash -c "sudo chmod 666 /dev/kvm && /bin/bash"
```

### Step 3: `make` SimBricks
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

### Step 4: Run gem5-based Experiments
`cd` to the directory `experiments/simbricks/`.
In here, you can find `run_*.sh` scripts to execute the individual experiments, grouped by the concrete hardware accelerator. Execute them like this:
```bash
bash run_protoacc.sh
```

### Step 5: `make` and Run NEX-based Experiments.
For instructions, take a look at `submodules/nex/README.md`.
