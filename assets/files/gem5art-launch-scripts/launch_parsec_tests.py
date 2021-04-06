import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance

packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.'
)

experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/darchr/gem5art-experiments.git',
    typ = 'git repo',
    name = 'parsec_tests',
    path =  './',
    cwd = '../',
    documentation = 'main repo to run parsec tests with gem5'
)

parsec_repo = Artifact.registerArtifact(
    command = '''mkdir parsec-benchmark/;
    cd parsec-benchmark;
    git clone https://github.com/darchr/parsec-benchmark.git;''',
    typ = 'git repo',
    name = 'parsec_repo',
    path =  './disk-image/parsec-benchmark/parsec-benchmark/',
    cwd = './disk-image/',
    documentation = 'main repo to copy parsec source to the disk-image'
)

gem5_repo = Artifact.registerArtifact(
    command = '''
        git clone https://gem5.googlesource.com/public/gem5;
        cd gem5;
        git remote add darchr https://github.com/darchr/gem5;
        git fetch darchr;
        git cherry-pick 6450aaa7ca9e3040fb9eecf69c51a01884ac370c;
        git cherry-pick 3403665994b55f664f4edfc9074650aaa7ddcd2c;
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 master branch from googlesource (Nov 18, 2019) and cherry-picked 2 commits from darchr/gem5'
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

disk_image = Artifact.registerArtifact(
    command = './packer build parsec/parsec.json',
    typ = 'disk image',
    name = 'parsec',
    cwd = 'disk-image',
    path = 'disk-image/parsec/parsec-image/parsec',
    inputs = [packer, experiments_repo, m5_binary, parsec_repo,],
    documentation = 'Ubuntu with m5 binary and PARSEC installed.'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary'
)

linux_repo = Artifact.registerArtifact(
    command = '''git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo'
)

linux_binary = Artifact.registerArtifact(
    name = 'vmlinux-4.19.83',
    typ = 'kernel',
    path = 'linux-stable/vmlinux-4.19.83',
    cwd = 'linux-stable/',
    command = '''
    cp ../config.4.19.83 .config;
    make -j8;
    cp vmlinux vmlinux-4.19.83;
    ''',
    inputs = [experiments_repo, linux_repo,],
    documentation = "kernel binary for v4.19.83"
)


if __name__ == "__main__":
    num_cpus = ['1']
    benchmarks = ['blackscholes', 'bodytrack', 'canneal', 'dedup','facesim', 'ferret', 'fluidanimate', 'freqmine', 'raytrace', 'streamcluster', 'swaptions', 'vips', 'x264']

    sizes = ['simsmall', 'simlarge', 'native']
    cpus = ['kvm', 'timing']

    for cpu in cpus:
        for num_cpu in num_cpus:
            for size in sizes:
                if cpu == 'timing' and size != 'simsmall':
                    continue
                for bm in benchmarks:
                    run = gem5Run.createFSRun(
                        'parsec_tests',    
                        'gem5/build/X86/gem5.opt',
                        'configs-parsec-tests/run_parsec.py',
                        f'''results/run_parsec/{bm}/{size}/{cpu}/{num_cpu}''',
                        gem5_binary, gem5_repo, experiments_repo,
                        'linux-stable/vmlinux-4.19.83',
                        'disk-image/parsec/parsec-image/parsec',
                        linux_binary, disk_image,
                        cpu, bm, size, num_cpu,
                        timeout = 24*60*60 #24 hours
                        )
                    run_gem5_instance.apply_async((run, os.getcwd(), ))
