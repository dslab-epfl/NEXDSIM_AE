import math
import os
import itertools

import simbricks.orchestration.experiments as exp
import simulators as sim
import nodeconfig as node
import appconfig as app

experiments = []

# Experiment parameters
host_variants = ["gt", "gk", "gem5_o3"]
vta_ops = ["rtl", "lpn"]
inference_device_opts = [
    node.TvmDeviceType.VTA,
    node.TvmDeviceType.CPU,
]
vta_clk_freq_opts = [100, 160, 200, 400, 800, 2000]
model_name_opts = [
    "resnet18_v1",
    "resnet34_v1",
    "resnet50_v1",
]
core_opts = [1, 4, 8, 16]


# Build experiment for all combinations of parameters
for (
    host_var,
    inference_device,
    vta_clk_freq,
    model_name,
    cores,
    vta_op,
) in itertools.product(
    host_variants,
    inference_device_opts,
    vta_clk_freq_opts,
    model_name_opts,
    core_opts,
    vta_ops,
):
    experiment = exp.Experiment(
        f"classify_160-{model_name}-{inference_device.value}-{host_var}-{vta_op}-{cores}-{vta_clk_freq}"
    )
    pci_vta_id = 5
    sync = False
    if host_var == "gt":
        HostClass = sim.Gem5MemSidechannelHost
        experiment.checkpoint = True
        sync = True
    elif host_var == "gk":
        HostClass = sim.Gem5KvmMemSidechannelHost
        sync = False
    elif host_var == "gem5_o3":
        HostClass = sim.Gem5O3MemSidechannelHost
        sync = True
        experiment.checkpoint = True

    # Instantiate server
    server_cfg = node.VtaNode()
    server_cfg.nockp = True
    server_cfg.cores = cores
    server_cfg.app = app.TvmClassifyLocal()
    server_cfg.app.device = inference_device
    server_cfg.app.model_name = model_name
    server_cfg.app.pci_vta_id = pci_vta_id
    server_cfg.app.gem5_cp = host_var in ["gt", "gem5_o3"]
    server = HostClass(server_cfg)
    # Whether to synchronize VTA and server
    server.sync = sync
    # Wait until server exits
    server.wait = True

    # Instantiate and connect VTA PCIe-based accelerator to server
    if inference_device == node.TvmDeviceType.VTA:

        if vta_op == "rtl":
            vta = sim.VTADev()
        else:
            vta = sim.VTALpnBmDev()
            if host_var == "gem5_o3":
                server.mem_sidechannels.append(vta)

        vta.clock_freq = vta_clk_freq
        server.add_pcidev(vta)

    server.pci_latency = server.sync_period = vta.pci_latency = vta.sync_period = 400

    # Add both simulators to experiment
    experiment.add_host(server)
    experiment.add_pcidev(vta)

    experiments.append(experiment)
