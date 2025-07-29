## Artifact Evaluation for paper "Fast End-to-End Performance Simulation of Accelerated Hardware-Software Stacks"

Following the guideline, you will be able to run experiments covering three accelerators VTA, Protoacc, JPEG with 4 different simulation modes, NEX+DSim, NEX+RTL, Gem5+DSim and Gem5+RTL.


1. Step 0, clone the repo
```bash
git clone https://github.com/dslab-epfl/NEXDSIM_AE.git
git submodule update --init --recursive
```

2. Step 1, setup nix enviroment
```
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
nix-shell --pure
```

3. Step 2, make simbricks
```
cd submodules/simbricks
make sims/external/gem5/ready
make sims/external/qemu/ready
make build-images
make convert-images-raw
make -C sims/external/vta/simbricks
make -C sims/external/protoacc/simbricks
make sims/misc/jpeg_decoder/jpeg_decoder_verilator
```

here we need to use `pkgs.gcc14` instead of `pkgs.gcc12`, replace the line in shell.nix temporaily, then build simbricks
```
cd submodules/simbricks
CC=gcc CXX=g++ make -j
```

<!--  
In the following, we will make RTL simulators, 

```bash
sudo apt install openjdk-17-jdk
```

In case you have java installed already, use the following one to choose the right version of java
```bash
sudo update-alternatives --config java 
sudo update-alternatives --config javac
```

install sbt

```bash
sudo apt-get update
sudo apt-get install apt-transport-https curl gnupg -yqq
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo -H gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/scalasbt-release.gpg --import
sudo chmod 644 /etc/apt/trusted.gpg.d/scalasbt-release.gpg
sudo apt-get update
sudo apt-get install sbt
```

```bash
unset TVM_PATH
unset VTA_HW_PATH
make -C sims/external/vta/simbricks
make -C sims/external/protoacc/simbricks
``` -->

4. Step 3, run gem5 based experiments


enter `sudo su`, then enter `nix-shell`
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


