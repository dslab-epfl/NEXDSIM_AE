# Copyright 2023 Max Planck Institute for Software Systems, and
# National University of Singapore
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import glob
import typing as tp

from PIL import Image

import simbricks.orchestration.experiments as exp
import simulators as sim
import nodeconfig as node
import appconfig as app

experiments: tp.List[exp.Experiment] = []
for host_var in ['gem5_kvm', 'gem5_o3', 'qemu_icount', 'qemu_kvm']:
    for jpeg_var in ['lpn', 'rtl']:
        e = exp.Experiment(f'jpeg_decoder-{host_var}-{jpeg_var}')
        node_cfg = node.NodeConfig()
        node_cfg.kcmd_append = 'memmap=512M!1G'
        dma_src = 1 * 1024**3
        dma_dst = dma_src + 10 * 1024**2
        node_cfg.memory = 2 * 1024
        # images = glob.glob('../sims/misc/jpeg_decoder/test_img/420/*.jpg')
        images = glob.glob('./jpeg_data/*.jpg')
        images.sort()
        node_cfg.app = app.JpegDecoderWorkload(
            '0000:00:05.0', images, dma_src, dma_dst, False
        )

        if host_var == 'gem5_kvm':
            host = sim.Gem5Host(node_cfg)
            host.cpu_type = 'X86KvmCPU'
        elif host_var == 'gem5_o3':
            e.checkpoint = True
            node_cfg.app.gem5_cp = True
            node_cfg.app.pci_device = '0000:00:05.0'
            host = sim.Gem5O3MemSidechannelHost(node_cfg)
            host.sync = True
            host.cpu_type = 'O3CPU'
            host.variant = 'fast'
            # host.modify_checkpoint_tick = False
        elif host_var == 'qemu_icount':
            node_cfg.app.pci_dev = '0000:00:02.0'
            host = sim.QemuHost(node_cfg)
            host.sync = True
        elif host_var == 'qemu_kvm':
            node_cfg.app.pci_dev = '0000:00:02.0'
            host = sim.QemuHost(node_cfg)
        else:
            raise NameError(f'Variant {host_var} is unhandled')
        host.wait = True
        e.add_host(host)

        if jpeg_var == 'lpn':
            jpeg_dev = sim.JpegDecoderLpnBmDev()
            if host_var == 'gem5_o3':
                host.mem_sidechannels.append(jpeg_dev)
        elif jpeg_var == 'rtl':
            jpeg_dev = sim.JpegDecoderDev()
        else:
            raise NameError(f'Variant {jpeg_var} is unhandled')
        
        jpeg_dev.name = 'jpeg0'
        jpeg_dev.clock_freq = 2000 # in Mhz

        host.add_pcidev(jpeg_dev)
        e.add_pcidev(jpeg_dev)

        host.pci_latency = host.sync_period = jpeg_dev.pci_latency = \
            jpeg_dev.sync_period = 400

        experiments.append(e)
