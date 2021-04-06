import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance

experiments_repo = Artifact.registerArtifact(
    command = '',
    typ = 'git repo',
    name = 'experiment',
    path =  './',
    cwd = './',
    documentation = 'local repo to run spec 2006 experiments with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = '''
        git clone -b v19.0.0.0 https://gem5.googlesource.com/public/gem5
        cd gem5
        scons build/X86/gem5.opt -j8
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 v19'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt -j8',
    typ = 'gem5 binary',
    name = 'gem5-19',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'compiled gem5 v19 binary'
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

packer = Artifact.registerArtifact(
    command = '''
        wget https://releases.hashicorp.com/packer/1.4.5/packer_1.4.5_linux_amd64.zip;
        unzip packer_1.4.5_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in November from hashicorp.'
)

disk_image = Artifact.registerArtifact(
    command = './packer build spec2006/spec2006.json',
    typ = 'disk image',
    name = 'spec2006',
    cwd = 'disk-image/',
    path = 'disk-image/spec2006/spec2006-image/spec2006',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu Server with SPEC 2006 installed, m5 binary installed and root auto login'
)

linux_repo = Artifact.registerArtifact(
    command = '''
        git clone git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/;
        mv linux linux-4.19.83
    ''',
    typ = 'git repo',
    name = 'linux-4.19.83',
    path =  'linux-4.19.83',
    cwd = './',
    documentation = 'Linux kernel 4.19 source code repo obtained in November'
)

linux_binary = Artifact.registerArtifact(
    name = 'vmlinux-4.19.83',
    typ = 'kernel',
    path = 'linux-4.19.83/vmlinux-4.19.83',
    cwd = './',
    command = '''
        cp linux-configs/config.4.19.83 linux-4.19.83/.config
        cd linux-4.19.83
        make -j8
        cp vmlinux vmlinux-4.19.83
    ''',
    inputs = [experiments_repo, linux_repo,],
    documentation = "kernel binary for v4.19.83",
)

run_script_repo = Artifact.registerArtifact(
    command = '''
        wget https://raw.githubusercontent.com/darchr/gem5art/master/docs/gem5-configs/configs-spec-tests/run_spec.py
        mkdir -p system
        cd system
        wget https://raw.githubusercontent.com/darchr/gem5art/master/docs/gem5-configs/configs-spec-tests/system/__init__.py
        wget https://raw.githubusercontent.com/darchr/gem5art/master/docs/gem5-configs/configs-spec-tests/system/caches.py
        wget https://raw.githubusercontent.com/darchr/gem5art/master/docs/gem5-configs/configs-spec-tests/system/fs_tools.py
        wget https://raw.githubusercontent.com/darchr/gem5art/master/docs/gem5-configs/configs-spec-tests/system/system.py
    ''',
    typ = 'git repo',
    name = 'gem5-configs',
    path =  'gem5-configs',
    cwd = './',
    documentation = 'gem5 run scripts made specifically for SPEC benchmarks'
)


if __name__ == "__main__":
    cpus = ['kvm', 'atomic', 'o3', 'timing']
    benchmark_sizes = {'kvm':    ['test', 'ref'],
                       'atomic': ['test'],
                       'o3':     ['test'],
                       'timing': ['test']
                      }
    benchmarks = ['401.bzip2','403.gcc','410.bwaves','416.gamess','429.mcf',
                  '433.milc','434.zeusmp','435.gromacs','436.cactusADM',
                  '437.leslie3d','444.namd','445.gobmk','453.povray',
                  '454.calculix','456.hmmer','458.sjeng','459.GemsFDTD',
                  '462.libquantum','464.h264ref','465.tonto','470.lbm',
                  '471.omnetpp','473.astar','481.wrf','482.sphinx3',
                  '998.specrand','999.specrand']
    # unavailable benchmarks: 400.perlbench,447.dealII,450.soplex,483.xalancbmk

    for cpu in cpus:
        for size in benchmark_sizes[cpu]:
            for benchmark in benchmarks:
                run = gem5Run.createFSRun(
                    'gem5 19 spec 2006 experiment', # name
                    'gem5/build/X86/gem5.opt', # gem5_binary
                    'gem5-configs/run_spec.py', # run_script
                    'results/{}/{}/{}'.format(cpu, size, benchmark), # relative_outdir
                    gem5_binary, # gem5_artifact
                    gem5_repo, # gem5_git_artifact
                    run_script_repo, # run_script_git_artifact
                    'linux-4.19.83/vmlinux-4.19.83', # linux_binary
                    'disk-image/spec2006/spec2006-image/spec2006', # disk_image
                    linux_binary, # linux_binary_artifact
                    disk_image, # disk_image_artifact
                    cpu, benchmark, size, # params
                    timeout = 5 * 24 * 60 * 60 # 5 days
                )
                run_gem5_instance.apply_async((run,))
