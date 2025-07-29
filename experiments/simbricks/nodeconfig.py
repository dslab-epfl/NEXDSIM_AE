import enum

from simbricks.orchestration.nodeconfig import *


class TvmDeviceType(enum.Enum):
    VTA = "vta"
    CPU = "cpu"

class VtaNode(NodeConfig):

    def __init__(self) -> None:
        super().__init__()
        # Use locally built disk image
        self.disk_image = "vta_classification"
        # Bump amount of system memory
        self.memory = 4 * 1024
        # Reserve physical range of memory for the VTA user-space driver
        # 1G is the start 1G - 1G+512M
        self.kcmd_append = "memmap=512M$1G iomem=relaxed"

    def prepare_pre_cp(self):
        # Define commands to run before application to configure the server
        cmds = super().prepare_pre_cp()
        cmds.extend(
            [
                "mount -t proc proc /proc",
                "mount -t sysfs sysfs /sys",
                # Make TVM's Python framework available
                "export PYTHONPATH=/root/tvm/python:${PYTHONPATH}",
                "export PYTHONPATH=/root/tvm/vta/python:${PYTHONPATH}",
                "export MXNET_HOME=/root/mxnet",
                # Set up loopback interface so the TVM inference script can
                # connect to the RPC server
                "ip link set lo up",
                "ip addr add 127.0.0.1/8 dev lo",
                "lspci -v",
                # Make VTA device available for control from user-space via
                # VFIO
                ("echo 1" " >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode"),
                'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id',
            ]
        )

        return cmds


class VtaNodeMulti(NodeConfig):

    def __init__(self) -> None:
        super().__init__()
        # Use locally built disk image
        self.disk_image = "vta_classification_multi"
        # Bump amount of system memory
        self.memory = 4 * 1024
        # Reserve physical range of memory for the VTA user-space driver
        # 1G is the start 1G - 1G+512M
        self.kcmd_append = "memmap=1G$1G iomem=relaxed"
        # self.kcmd_append = "memmap=512M@1G iomem=relaxed"
        # self.kcmd_append = "iomem=relaxed"

    def prepare_pre_cp(self):
        # Define commands to run before application to configure the server
        cmds = super().prepare_pre_cp()
        cmds.extend([
            "mount -t proc proc /proc",
            "mount -t sysfs sysfs /sys",
            "mkdir /dev/shm",
            "mount -t tmpfs tmpfs /dev/shm",
            # Make TVM's Python framework available
            "export PYTHONPATH=/root/tvm/python:${PYTHONPATH}",
            "export PYTHONPATH=/root/tvm/vta/python:${PYTHONPATH}",
            "export MXNET_HOME=/root/mxnet",
            # Set up loopback interface so the TVM inference script can
            # connect to the RPC server
            "ip link set lo up",
            "ip addr add 127.0.0.1/8 dev lo",
            # Make VTA device available for control from user-space via
            # VFIO
            (
                "echo 1"
                " >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode"
            ),
            'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id',
        ])

        return cmds

class VtaNodeDetect(NodeConfig):

    def __init__(self) -> None:
        super().__init__()
        # Use locally built disk image
        self.disk_image = "vta_detect"
        # Bump amount of system memory
        self.memory = 3 * 1024
        # Reserve physical range of memory for the VTA user-space driver
        self.kcmd_append = " memmap=512M!1G"
        self.nockp = True

    def prepare_pre_cp(self):
        # Define commands to run before application to configure the server
        cmds = super().prepare_pre_cp()
        cmds.extend([
            "mount -t proc proc /proc",
            "mount -t sysfs sysfs /sys",
            # Make TVM's Python framework available
            "export PYTHONPATH=/root/tvm/python:${PYTHONPATH}",
            "export PYTHONPATH=/root/tvm/vta/python:${PYTHONPATH}",
            # Set up loopback interface so the TVM inference script can
            # connect to the RPC server
            "ip link set lo up",
            "ip addr add 127.0.0.1/8 dev lo",
            # Make VTA device available for control from user-space via
            # VFIO
            (
                "echo 1"
                " >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode"
            ),
            'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id',
        ])
        return cmds

