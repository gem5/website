#!/usr/bin/env python3

#This is a job launch script

import os
import sys
from uuid import UUID

from gem5art.artifact.artifact import Artifact
from gem5art.run import gem5Run
from gem5art import tasks

"""packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.'
)"""

experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/darchr/microbenchmark-experiments.git',
    typ = 'git repo',
    name = 'microbenchmark-tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run microbenchmarks with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/darchr/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'git repo with gem5 master branch on Sep 23rd'
)

m5_binary = Artifact.registerArtifact(
    command = 'make -f Makefile.x86',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

"""disk_image = Artifact.registerArtifact(
    command = 'packer build template.json',
    typ = 'disk image',
    name = 'boot-disk',
    cwd = 'disk-image',
    path = 'disk-image/boot-exit/boot-exit-image/boot-exit',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu with m5 binary installed and root auto login'
)"""

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'default gem5 x86'
)

"""linux_repo = Artifact.registerArtifact(
    command = '''git clone https://github.com/torvalds/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo from Sep 23rd'
)"""

#linuxes = ['5.2.3']#, '4.14.134', '4.9.186', '4.4.186']
"""linux_binaries = {
    version: Artifact.registerArtifact(
                name = f'vmlinux-{version}',
                typ = 'kernel',
                path = f'linux-stable/vmlinux-{version}',
                cwd = 'linux-stable/',
                command = f'''git checkout v{version};
                cp ../linux-configs/config.{version} .config;
                make -j8;
                cp vmlinux vmlinux-{version};
                '''.format(v='5.2.3'),
                inputs = [experiments_repo, linux_repo,],
                documentation = f"Kernel binary for {version} with simple "
                                 "config file",
            )
    for version in linuxes
}"""

if __name__ == "__main__":
    #boot_types = ['init']#, 'systemd']
    num_cpus = ['1']#, '2', '4', '8']
    cpu_types = ['kvm']#, 'atomic', 'simple', 'o3']
    mem_types = ['classic']#, 'ruby']
    #configuration needed to run
    config='config1' #'config2''config3'
    #type of benchmark
    benchmark='microbenchmark'
    #benchmark list to run
    Controlbenchmarks=('MC','MCS')
    bm_list=[]
    bm_list=list(Controlbenchmarks)

    #Architecture to run with.
    arch='X86' #'ARM'
    if arch =='X86':
        bm='bench.X86'
    elif arch =='ARM':
        bm='bench.ARM'

    #For configuration 2:
    #Branchpredictors with a cpu
    Simple_configs=('Simple_Local', 'Simple_BiMode', 'Simple_Tournament', 'Simple_LTAGE')
    DefaultO3_configs=('DefaultO3_Local' ,'DefaultO3_BiMode', 'DefaultO3_Tournament','DefaultO3_LTAGE')
    Minor_configs=('Minor_Local', 'Minor_BiMode', 'Minor_Tournament', 'Minor_LTAGE')
    cpu_bp='simple'
    
    #For configuration 3:
    #Cache_type:
    cache_type = 'L1_cache' #'L2_cahe'
    #L1Cache_sizes.
    L1D = ['32kB','128kB','64kB']
    #L2Cache_sizes.
    L2C = ['1MB','512kB']

    if config == 'config1':
        if benchmark == 'microbenchmark':
            for mem in mem_types:
                for bms  in bm_list:
                    for cpu in cpu_types:
                            run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_config1.py',
                                gem5_binary, gem5_repo, experiments_repo,
                                cpu, mem, '../benchmarks/microbench/bms/bm'
                                    )
                            run_gem5_instance.apply_async((run,))
        elif benchmark == 'spec':
            for mem in mem_types:
                for bms  in bm_list:
                    for cpu in cpu_types:
                            run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_spec.py',
                                gem5_binary, gem5_repo, experiments_repo,
                                cpu, mem, '../benchmarks/microbench/bms/bm'
                                    )
                            run_gem5_instance.apply_async((run,))

    elif config == 'config2':
        for mem in mem_types:
            for bms in bm_list:
                if cpu_bp == 'simple':
                    for config_cpu in Simple_configs:
                        run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_spec.py',
                                gem5_binary, gem5_repo, experiments_repo,
                                config_cpu, mem, '../benchmarks/microbench/bms/bm'
                                    )
                        run_gem5_instance.apply_async((run,))
                elif cpu_bp == 'o3':
                    for config_cpu in Simple_configs:
                        run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_spec.py',
                                gem5_binary, gem5_repo, experiments_repo,
                                config_cpu, mem, '../benchmarks/microbench/bms/bm'
                                    )
                        run_gem5_instance.apply_async((run,))
            

    elif config =='config3':
        for mem in mem_types:
            for bms  in bm_list:
                for cpu in cpu_types:
                        if cache_type=='L1_cache':
                            for size in L1D:
                                run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_config1.py',
                                gem5_binary, gem5_repo, experiments_repo,
                                cpu, mem, '..benchmarks/microbench/bms/bm', 
                                    )
                                run_gem5_instance.apply_async((run,))
                        elif cache_type=='L2_cache':
                            for size in L2C:
                                run = gem5Run.createSERun(
                                'gem5/build/X86/gem5.opt',
                                'configs-boot-tests/run_config1.py',
                                gem5_binary,gem5_repo, experiment_repo,
                                cpu,mrm, '..benchmarks.microbench/bms/bm'
                                    )
                                run_gem5_instance.apply_asynch((run,))

                

    



    

