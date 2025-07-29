import math
import os
import typing as tp

import exps_common
import nodeconfig as node
from typing import List
import glob
from PIL import Image

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
        cmds.append(
            (
                "python3 /tmp/guest/deploy_classification-infer.py /root/mxnet"
                f" {self.device.value} {self.model_name} /tmp/guest/cat.png"
                f" {self.batch_size} {self.repetitions} {int(self.debug)} 0"
            ),
        )

        print(cmds)
        return cmds

class TvmClassifyMulti(node.AppConfig):
    """Runs inference for detection model locally, either on VTA or the CPU."""

    def __init__(self):
        super().__init__()
        self.pci_vta_id_start = 0
        self.num_vta_devices = 1
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
            "pci_driver.cc":
                open(
                    f"{exps_common.dir_simbricks}/local/tvm/3rdparty/vta-hw/src/simbricks-pci/pci_driver.cc.100MB",
                    "rb",
                ),
            "test.c":
                open(
                    f"{exps_common.dir_simbricks}/local/test.c",
                    "rb",
                ),
            "cat.png":
                open(f"{exps_common.dir_simbricks}/local/data/cat.png", "rb"),
            "multi_classification-infer.py":
                open(
                    f"{exps_common.dir_simbricks}/local/tvm/vta/tutorials/frontend/multi_classification-infer.py",
                    "rb"
                )
        }

    def prepare_pre_cp(self):
        cmds = super().prepare_pre_cp()
        cmds.extend([
            'echo \'{"TARGET" : "simbricks-pci", "HW_VER" : "0.0.2",'
            ' "LOG_INP_WIDTH" : 3, "LOG_WGT_WIDTH" : 3,'
            ' "LOG_ACC_WIDTH" : 5, "LOG_BATCH" :'
            f' {int(math.log2(self.vta_batch))}, "LOG_BLOCK" :'
            f' {int(math.log2(self.vta_block))}, "LOG_UOP_BUFF_SIZE" :'
            ' 15, "LOG_INP_BUFF_SIZE" : 15, "LOG_WGT_BUFF_SIZE" : 18,'
            ' "LOG_ACC_BUFF_SIZE" : 17 }\' >'
            " /root/tvm/3rdparty/vta-hw/config/vta_config.json"
        ])
        return cmds

    def run_cmds(self, node):
        # define commands to run on simulated server
        cmds = []
        cmds.extend([
            # start RPC server
            f"export TVM_NUM_THREADS=1 ",
            f"python3 -m tvm.exec.rpc_tracker --host=0.0.0.0 --port=9091 &",
            "sleep 30"
        ])
        for i in range(self.num_vta_devices):
            cmds.append(
                f"VTA_DEVICE=0000:00:{(self.pci_vta_id_start + i):02x}.0 VTA_VFIO_GROUP_ID={i} python3 -m vta.exec.rpc_server --key=simbricks-pci --tracker=127.0.0:9091 &"
            )
            cmds.append(
               "sleep 2"
            )
        cmds.extend([
            # wait for RPC servers to start
            "sleep 30",
        ])
        cmds.extend([
            # wait for RPC servers to start
            "python3 -m tvm.exec.query_rpc_tracker --host 0.0.0.0 --port 9091",
        ])
        if self.gem5_cp:
            cmds.append("export GEM5_CP=1")
        # cmds.extend([
        #     "dmesg | grep -i mtrr",
        #     "dmesg | grep -i pat"])
        # run inference
        cmds.append((
            "python3 /tmp/guest/multi_classification-infer.py /root/mxnet"
            f" {self.device.value} {self.model_name} /tmp/guest/cat.png"
            f" {self.batch_size} {self.repetitions} {int(self.debug)} 0 {self.num_vta_devices}"
        ))

        return cmds


class TvmDetectLocal(node.AppConfig):
    """Runs inference for detection model locally, either on VTA or the CPU."""

    def __init__(self):
        super().__init__()
        self.pci_vta_id = 0
        self.device = node.TvmDeviceType.VTA
        self.test_img = "person.jpg"
        self.repetitions = 1
        self.batch_size = 1
        self.debug = False
        """Whether to dump inference result."""

    def config_files(self):
        # mount TVM inference script in simulated server under /tmp/guest
        return {
            "deploy_detection-infer.py":
                open(
                    f"{exps_common.dir_simbricks}/local/tvm/vta/tutorials/frontend/deploy_detection-infer.py",
                    "rb",
                )
        }

    def run_cmds(self, node):
        # define commands to run on simulated server
        cmds = [
            f"export TVM_NUM_THREADS=1 ",
            # start RPC server
            f"VTA_DEVICE=0000:00:{(self.pci_vta_id):02d}.0 VTA_VFIO_GROUP_ID=0 python3 -m"
            " vta.exec.rpc_server &"
            # wait for RPC server to start
            "sleep 6",
            f"export VTA_RPC_HOST=127.0.0.1",
            f"export VTA_RPC_PORT=9091"
        ]
        if self.gem5_cp:
            cmds.append("export GEM5_CP=1")

        cmds.append(
            # run inference
            (
                "python3 /tmp/guest/deploy_detection-infer.py "
                "/root/darknet"
                f" {self.device.value} {self.test_img} {self.batch_size} "
                f"{self.repetitions} {int(self.debug)} 0"
            )
        )

        print(cmds)
        # dump image with detection boxes as base64 to allow later inspection
        if self.debug:
            cmds.extend([
                "echo dump deploy_detection-infer-result.png START",
                "base64 deploy_detection-infer-result.png",
                "echo dump deploy_detection-infer-result.png END",
            ])
        return cmds

class VTAMatMul(node.AppConfig):

    def __init__(self, pci_device: str) -> None:
        super().__init__()
        self.pci_device = pci_device
        self.gem5_cp = False
        """Whether to use fine-grained gem5 checkpointing."""

    def config_files(self) -> tp.Dict[str, tp.IO]:
        return {
            'matrix_multiply_opt.py':
                open(
                    f'{exps_common.dir_simbricks}/local/tvm/vta/tutorials/optimize/matrix_multiply_opt.py',
                    'rb'
                ),
        }

    def prepare_pre_cp(self) -> tp.List[str]:
        return [
            f"export TVM_NUM_THREADS=1 ",
            f'export GEM5_CP={int(self.gem5_cp)}',
            f'export VTA_DEVICE={self.pci_device}',
            'export VTA_VFIO_GROUP_ID=0',
            'export VTA_RPC_HOST=127.0.0.1',
            'export VTA_RPC_PORT=9091',
            # this only starts the RPC server, the driver for VTA is only loaded
            # once VTA is actually invoked
            '/usr/bin/python3 -m vta.exec.rpc_server --host=${VTA_RPC_HOST} --port=${VTA_RPC_PORT} &',
            # the RPC server takes quite long to start, ofte more than 5 s
            'sleep 5',
            'python /tmp/guest/matrix_multiply_opt.py'
        ]

    def run_cmds(self, node):
        return []


class ProtoaccBenchmark(node.AppConfig):

    def __init__(self, pci_device: str, which_bench:str) -> None:
        super().__init__()
        self.pci_device = pci_device
        self.which_bench = which_bench

    def config_files(self):
        return {
            "benchmark.x86":
                open(
                    f"{exps_common.dir_simbricks}/local/hyperprotobench/gem5/{self.which_bench}-ser/benchmark.x86",
                    "rb",
                )
        }

    def prepare_pre_cp(self):
        cmds = super().prepare_pre_cp()
        cmds.extend([
            f'export PROTOACC_DEVICE={self.pci_device}',
            ]
        )
        return cmds
    
    def run_cmds(self, node) -> List[str]:
        cmds = ["cd /tmp/guest && ./benchmark.x86"]
        cmds.append("time ./benchmark.x86")
        cmds.append("ls")
        return cmds


class JpegDecoderWorkload(node.AppConfig):

    def __init__(
        self,
        pci_dev: str,
        images: tp.List[str],
        dma_src_addr: int,
        dma_dst_addr: int,
        debug: bool
    ) -> None:
        super().__init__()
        self.pci_dev = pci_dev
        self.images = images
        self.dma_src_addr = dma_src_addr
        self.dma_dst_addr = dma_dst_addr
        self.debug = debug

    def prepare_pre_cp(self) -> tp.List[str]:
        return [
            'mount -t proc proc /proc',
            'mount -t sysfs sysfs /sys',
            'echo 1 >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode',
            'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id',
        ]

    def run_cmds(self, node: node.NodeConfig) -> tp.List[str]:
        # enable vfio access to JPEG decoder
        cmds = []

        for img in self.images:
            with Image.open(img) as loaded_img:
                width, height = loaded_img.size

            cmds.extend([
                f'echo starting decode of image {os.path.basename(img)}',
                # copy image into memory
                (
                    f'dd if=/tmp/guest/{os.path.basename(img)} bs=4096 '
                    f'of=/dev/mem seek={self.dma_src_addr} oflag=seek_bytes '
                ),
                # invoke workload driver
                (
                    f'/tmp/guest/jpeg_decoder_workload_driver {self.pci_dev} '
                    f'{self.dma_src_addr} {os.path.getsize(img)} '
                    f'{self.dma_dst_addr}'
                ),
                f'echo finished decode of image {os.path.basename(img)}',
            ])

            if self.debug:
                # dump the image as base64 to stdout
                cmds.extend([
                    f'echo image dump begin {width} {height}',
                    (
                        f'dd if=/dev/mem iflag=skip_bytes,count_bytes bs=4096 '
                        f'skip={self.dma_dst_addr} count={width * height * 2} '
                        'status=none | base64'
                    ),
                    'echo image dump end'
                ])
        return cmds

    def config_files(self) -> tp.Dict[str, tp.IO]:
        files = {
            'jpeg_decoder_workload_driver':
                open(
                    f'{exps_common.dir_project_root}/dsim/jpeg_decoder/jpeg_decoder_workload_driver',
                    'rb'
                )
        }

        for img in self.images:
            files[os.path.basename(img)] = open(img, 'rb')

        return files


class JpegDecoderWorkloadMulti(node.AppConfig):

    def __init__(
        self,
        dma_addr_start : int,
        num_decoders: int
    ) -> None:
        super().__init__()
        self.dma_addr_start = dma_addr_start
        self.num_decoders = num_decoders

    def prepare_pre_cp(self) -> tp.List[str]:
        return [
            'mount -t proc proc /proc',
            'mount -t sysfs sysfs /sys',
            # enable vfio access to JPEG decoder
            'echo 1 >/sys/module/vfio/parameters/enable_unsafe_noiommu_mode',
            'echo "dead beef" >/sys/bus/pci/drivers/vfio-pci/new_id',
            'sleep 5',
        ]

    def run_cmds(self, node: node.NodeConfig) -> tp.List[str]:
        cmds = []
        cmds.append(f"/tmp/guest/jpeg_multithreaded_workload 5 {self.num_decoders} {self.dma_addr_start}")
        return cmds

    def config_files(self) -> tp.Dict[str, tp.IO]:
        files = {}
        print("DEBUG FILE PATH", f"{exps_common.dir_simbricks}/sims/misc/jpeg_decoder/jpeg_multithreaded_workload")
        
        files["jpeg_multithreaded_workload"] = open(f"{exps_common.dir_simbricks}/sims/misc/jpeg_decoder/jpeg_multithreaded_workload", 'rb')

        for img in sorted(glob.glob("./jpeg_data/*.jpg")):
            files[os.path.basename(img)] = open(img, 'rb')

        return files



