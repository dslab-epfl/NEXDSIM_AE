# Copyright 2024 Max Planck Institute for Software Systems, and
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

from typing import List
import simbricks.orchestration.experiments as exp
import simulators as sim
import nodeconfig as node
import appconfig as app

experiments = []
host_sim_choices = ["gem5_o3", "gem5_kvm", "qemu_kvm"]
which_bench = ["bench0","bench1","bench2","bench3","bench4","bench5", "b1s"]
rtl_mode = ['rtl', 'lpn']

for acc_mode in rtl_mode: 
    for host_sim in host_sim_choices:
        for this_bench in which_bench:
            e = exp.Experiment(f"protoacc_benchmark-{acc_mode}-{host_sim}-{this_bench}")
            e.checkpoint = True
            node_config = node.VtaNode()
            node_config.cores = 1
            
            node_config.app = app.ProtoaccBenchmark('0000:00:05.0', this_bench)

            if host_sim == "gem5_kvm":
                node_config.app.pci_device = '0000:00:00.0'
                e.checkpoint = False
                host = sim.Gem5Host(node_config)
                host.cpu_type = 'X86KvmCPU'
                host.name = 'host0'
                host.sync = True
                host.wait = True
            elif host_sim == "gem5_o3":
                host = sim.Gem5O3MemSidechannelHost(node_config)
                node_config.app.pci_device = '0000:00:05.0'
                e.checkpoint = True
                host.cpu_type = 'O3CPU'
                host.cpu_type_cp = "X86AtomicSimpleCPU"
                host.variant = 'fast'
                host.cpu_freq = '3GHz'
                host.name = 'host0'
                host.sync = True
                host.wait = True
            elif host_sim == "qemu_kvm":
                host = sim.QemuHost(node_config)
            
            if acc_mode == "rtl":
                pac = sim.ProtoaccDev()
            elif acc_mode == "lpn":
                pac = sim.ProtoaccLpnBmDev()

            pac.name = 'pac0'
            pac.clock_freq = 2000
            host.add_pcidev(pac)

            if acc_mode == "lpn" and host_sim == "gem5_o3":
                host.mem_sidechannels.append(pac)

            pac.pci_latency = pac.sync_period = host.pci_latency = \
                host.sync_period = host.pci_latency = host.sync_period = 4 # 4ns
            e.add_pcidev(pac)

            e.add_host(host)

            experiments.append(e)
