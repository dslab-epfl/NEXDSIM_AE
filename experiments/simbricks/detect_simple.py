import os
import sys

import simbricks.orchestration.experiments as exp
import simulators as sim
import nodeconfig as node
import appconfig as app
import itertools
    
experiments = []

# Experiment parameters
host_variants = ["qemu_kvm", "qemu_icount", "gem5_o3"]
vta_ops = ["rtl", "lpn"]
inference_device_opts = [node.TvmDeviceType.CPU, node.TvmDeviceType.VTA]
vta_clk_freq_opts = [100, 160, 200, 400, 2000]

# Build experiment for all combinations of parameters
for host_var, inference_device, vta_clk_freq, vta_op in itertools.product(
    host_variants, inference_device_opts, vta_clk_freq_opts, vta_ops
):
    experiment = exp.Experiment(
        f"detect-{inference_device.value}-{host_var}-{vta_op}-{vta_clk_freq}"
    )
    pci_vta_id = 5
    sync = False
    if host_var == "qemu_kvm":
        HostClass = sim.QemuHost
    elif host_var == "qemu_icount":
        HostClass = sim.QemuIcountHost
        sync = True
    elif host_var == "gem5_o3":
        HostClass = sim.Gem5O3MemSidechannelHost
        sync = True
        experiment.checkpoint = True

    #######################################################
    # Define and connect all simulators
    # -----------------------------------------------------
    # Instantiate server
    server_cfg = node.VtaNodeDetect()
    server_cfg.cores = 4
    server_cfg.app = app.TvmDetectLocal()
    server_cfg.app.pci_vta_id = pci_vta_id
    server_cfg.app.gem5_cp = host_var in ["gem5_o3"]
    server = HostClass(server_cfg)
    # Whether to synchronize VTA and server
    server.sync = sync
    # Wait until server exits
    server.wait = True

    # Instantiate and connect VTA PCIe-based accelerator to server
    if vta_op == "rtl":
        vta = sim.VTADev()
    else:
        vta = sim.VTALpnBmDev()
        if host_var == "gem5_o3":
            server.mem_sidechannels.append(vta)

    vta.clock_freq = vta_clk_freq
    server.add_pcidev(vta)

    server.pci_latency = server.sync_period = vta.pci_latency = (
        vta.sync_period
    ) = 400

    # Add both simulators to experiment
    experiment.add_host(server)
    experiment.add_pcidev(vta)

    experiments.append(experiment) 

