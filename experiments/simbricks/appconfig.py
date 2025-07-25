import math
import os
import typing as tp

import exps_common
import nodeconfig as node


class TvmClassifyLocal(node.AppConfig):
    """Runs inference for detection model locally, either on VTA or the CPU."""

    def __init__(self):
        super().__init__()
        self.pci_vta_id = 0
        self.device = node.TvmDeviceType.VTA
        self.repetitions = 1
        self.batch_size = 1
        self.vta_batch = 1
        self.vta_block = 16
        self.model_name = "resnet18_v1"
        self.debug = True
        self.gem5_cp = False

    def config_files(self):
        # mount TVM inference script in simulated server under /tmp/guest
        return {
            "pci_driver.cc": open(
                f"{exps_common.dir_simbricks}/local/pci_driver.cc",
                "rb",
            ),
            "test.c": open(
                f"{exps_common.dir_simbricks}/local/test.c",
                "rb",
            ),
            "deploy_classification-infer.py": open(
                f"{exps_common.dir_simbricks}/local/tvm/vta/tutorials/frontend/deploy_classification-infer.py",
                "rb",
            ),
            "cat.png": open(f"{exps_common.dir_simbricks}/local/data/cat.png", "rb"),
        }

    def prepare_pre_cp(self):
        cmds = super().prepare_pre_cp()
        cmds.extend(
            [
                'echo \'{"TARGET" : "simbricks-pci", "HW_VER" : "0.0.2",'
                ' "LOG_INP_WIDTH" : 3, "LOG_WGT_WIDTH" : 3,'
                ' "LOG_ACC_WIDTH" : 5, "LOG_BATCH" :'
                f' {int(math.log2(self.vta_batch))}, "LOG_BLOCK" :'
                f' {int(math.log2(self.vta_block))}, "LOG_UOP_BUFF_SIZE" :'
                ' 15, "LOG_INP_BUFF_SIZE" : 15, "LOG_WGT_BUFF_SIZE" : 18,'
                ' "LOG_ACC_BUFF_SIZE" : 17 }\' >'
                " /root/tvm/3rdparty/vta-hw/config/vta_config.json"
            ]
        )
        return cmds

    def run_cmds(self, node):
        # define commands to run on simulated server
        # cmds = [
        # "cp /tmp/guest/pci_driver.cc /root/tvm/3rdparty/vta-hw/src/simbricks-pci/pci_driver.cc",
        # "cd /root/tvm/build",
        # "make clean",
        # "make -j4",
        # ]
        cmds = []
        cmds.extend(
            [
                # start RPC server
                f"export TVM_NUM_THREADS=1 ",
                f"VTA_DEVICE=0000:00:{(self.pci_vta_id):02d}.0 VTA_VFIO_GROUP_ID=0 python3 -m"
                " vta.exec.rpc_server &"
                # wait for RPC server to start
                "sleep 6",
                f"export VTA_RPC_HOST=127.0.0.1",
                f"export VTA_RPC_PORT=9091",
            ]
        )
        if self.gem5_cp:
            cmds.append("export GEM5_CP=1")
        # cmds.extend([
        #     "dmesg | grep -i mtrr",
        #     "dmesg | grep -i pat"])
        # run inference
        cmds.append(
            (
                "python3 /tmp/guest/deploy_classification-infer.py /root/mxnet"
                f" {self.device.value} {self.model_name} /tmp/guest/cat.png"
                f" {self.batch_size} {self.repetitions} {int(self.debug)} 0"
            ),
        )

        print(cmds)
        return cmds
