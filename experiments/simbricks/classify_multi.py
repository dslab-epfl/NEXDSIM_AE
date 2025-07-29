import math
import simbricks.orchestration.experiments as exp
import simulators as sim
import nodeconfig as node
import appconfig as app
import itertools

experiments = []

# Experiment parameters
host_variants = ["gk", "go3"]
vta_ops = ["rtl", "lpn"]
inference_device_opts = [
    node.TvmDeviceType.VTA,
    node.TvmDeviceType.CPU,
]

model_name_opts = [
    "resnet18_v1",
    "resnet34_v1",
    "resnet50_v1",
]
num_vta_opts = [1, 2, 4, 8]

# Build experiment for all combinations of parameters
for (
    host_var,
    inference_device,
    model_name,
    vta_op,
    num_vta
) in itertools.product(
    host_variants,
    inference_device_opts,
    model_name_opts,
    vta_ops,
    num_vta_opts
):
    experiment = exp.Experiment(
        f"classify_multi-{model_name}-{inference_device.value}-{host_var}-{vta_op}-{num_vta}"
    )
    

    # Instantiate server
    HostClass = sim.Gem5O3MemSidechannelHost
    server_cfg = node.VtaNodeMulti()
    server_cfg.nockp = True
    server_cfg.cores = 8
    server_cfg.app = app.TvmClassifyMulti()
    server_cfg.app.device = inference_device
    server_cfg.app.model_name = model_name
    server_cfg.app.pci_vta_id_start = 5
    server_cfg.app.gem5_cp = True
    server_cfg.app.num_vta_devices = num_vta
    server = HostClass(server_cfg)
    # Whether to synchronize VTA and server
    if host_var == "gk":
        server.cpu_type = 'X86KvmCPU'
        server.sync = False
    elif host_var == "go3":
        server.sync = True
        experiment.checkpoint = True
    # Wait until server exits
    server.wait = True

    pci_latency = 400

    # Instantiate and connect VTA PCIe-based accelerator to server
    if inference_device == node.TvmDeviceType.VTA:
        for i in range(num_vta):
            if vta_op == "rtl":
                vta = sim.VTADev()
            else:
                vta = sim.VTALpnBmDev()
                server.mem_sidechannels.append(vta)

            vta.clock_freq = 2000
            vta.name = f"vta{i}"
            vta.pci_latency = vta.sync_period = pci_latency
            server.add_pcidev(vta)

    server.pci_latency = server.sync_period = pci_latency

    # Add both simulators to experiment
    experiment.add_host(server)
    experiment.add_pcidev(vta)

    experiments.append(experiment)
