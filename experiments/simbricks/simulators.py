import exps_common
from simbricks.orchestration.experiment.experiment_environment import ExpEnv
from simbricks.orchestration.simulators import *


class Gem5MemSidechannelHost(Gem5Host):

    def __init__(self, node_config: NodeConfig) -> None:
        super().__init__(node_config)
        self.cpu_freq = "3GHz"
        self.mem_sidechannels = []
        self.variant = "fast"

    def run_cmd(self, env: ExpEnv) -> str:
        cmd = super().run_cmd(env)
        cmd += " "

        for mem_sidechannel in self.mem_sidechannels:
            cmd += (
                "--simbricks-mem_sidechannel=connect"
                f":{env.dev_mem_path(mem_sidechannel)}"
            )
            cmd += " "
        return cmd


class Gem5KvmMemSidechannelHost(Gem5MemSidechannelHost):

    def __init__(self, node_config: NodeConfig) -> None:
        super().__init__(node_config)
        self.cpu_type = "X86KvmCPU"


class Gem5O3MemSidechannelHost(Gem5MemSidechannelHost):

    def __init__(self, node_config: NodeConfig) -> None:
        super().__init__(node_config)
        self.cpu_type = "O3CPU"


class VTADev(PCIDevSim):

    def __init__(self) -> None:
        super().__init__()
        self.clock_freq = 100
        """Clock frequency in MHz"""

    def run_cmd(self, env):
        cmd = (
            f"{env.repodir}/sims/external/vta/simbricks/vta_simbricks "
            f"{env.dev_pci_path(self)} {env.dev_shm_path(self)} "
            f"{self.start_tick} {self.sync_period} {self.pci_latency} "
            f"{self.clock_freq}"
        )
        return cmd


class ProtoaccDev(PCIDevSim):

    def __init__(self) -> None:
        super().__init__()
        self.clock_freq = 2000
        """Clock frequency in MHz"""

    def run_cmd(self, env):
        cmd = (
            f"{env.repodir}/sims/misc/protoacc/simbricks/protoacc_simbricks "
            f"{env.dev_pci_path(self)} {env.dev_shm_path(self)} "
            f"{self.start_tick} {self.sync_period} {self.pci_latency} "
            f"{self.clock_freq}"
        )
        return cmd


class VTALpnBmDev(PCIDevSim):
    """Behavioral model of the VTA based on a Latency Petri Net."""

    def __init__(self) -> None:
        super().__init__()
        self.start_tick = 0
        self.name = "vta_lb"
        self.deps = []

    def resreq_mem(self) -> int:
        return 512  # this is a guess

    def run_cmd(self, env: ExpEnv) -> str:
        return (
            f"{exps_common.dir_project_root}/dsim/vta/vta_bm "
            f"{env.dev_mem_path(self)} {env.dev_shm_path(self)}_ms "
            f"{env.dev_pci_path(self)} {env.dev_shm_path(self)} "
            f"{self.start_tick} {self.sync_period} {self.pci_latency} "
        )

    def dependencies(self) -> list[Simulator]:
        return self.deps

    def sockets_wait(self, env: ExpEnv) -> list[str]:
        wait = super().sockets_wait(env)
        wait.append(env.dev_mem_path(self))
        return wait


class ProtoaccLpnBmDev(PCIDevSim):
    """Behavioral model of the VTA based on a Latency Petri Net."""

    def __init__(self) -> None:
        super().__init__()
        self.start_tick = 0
        self.name = "pac_lb"
        self.deps = []

    def resreq_mem(self) -> int:
        return 512  # this is a guess

    def run_cmd(self, env: ExpEnv) -> str:
        return (
            f"{exps_common.dir_project_root}/dsim/protoacc/protoacc_bm "
            f"{env.dev_mem_path(self)} {env.dev_shm_path(self)}_ms "
            f"{env.dev_pci_path(self)} {env.dev_shm_path(self)} "
            f"{self.start_tick} {self.sync_period} {self.pci_latency} "
        )

    def dependencies(self) -> list[Simulator]:
        return self.deps

    def sockets_wait(self, env: ExpEnv) -> list[str]:
        wait = super().sockets_wait(env)
        wait.append(env.dev_mem_path(self))
        return wait


class JpegDecoderLpnBmDev(PCIDevSim):
    """Behavioral model of the JPEG decoder based on a Latency Petri Net."""

    def __init__(self) -> None:
        super().__init__()
        self.start_tick = 0
        self.name = "jpeg_lb"
        self.deps = []

    def resreq_mem(self) -> int:
        return 512  # this is a guess

    def run_cmd(self, env: ExpEnv) -> str:
        return (
            f"{exps_common.dir_project_root}/dsim/jpeg_decoder/jpeg_decoder_bm "
            f"{env.dev_mem_path(self)} {env.dev_shm_path(self)}_ms "
            f"{env.dev_pci_path(self)} {env.dev_shm_path(self)} "
            f"{self.start_tick} {self.sync_period} {self.pci_latency} "
        )

    def dependencies(self) -> list[Simulator]:
        return self.deps

    def sockets_wait(self, env: ExpEnv) -> list[str]:
        wait = super().sockets_wait(env)
        wait.append(env.dev_mem_path(self))
        return wait
