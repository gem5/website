#!/usr/bin/env python3

#This is a job launch script for boot tests

import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance

experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/micro-tests.git',
    typ = 'git repo',
    name = 'micro-tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run microbenchmarks with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = '''git clone https://gem5.googlesource.com/public/gem5;
    cd gem5;
    wget https://github.com/darchr/gem5/commit/38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch;
    git am 38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch --reject;
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'git repo with gem5 cloned on Nov 22 from googlesource (patch applied to support mem vector port)'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'default gem5 x86'
)

if __name__ == "__main__":

    cpu_types = ['TimingSimple', 'DerivO3']
    mem_types = ['Inf', 'SingleCycle', 'Slow']

    bm_list = []

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    for filename in os.listdir('microbench'):
        if os.path.isdir(f'microbench/{filename}') and filename != '.git':
            bm_list.append(filename)

    # create an artifact for each single microbenchmark
    for bm in bm_list:
        bm = Artifact.registerArtifact(
        command = '''
        cd microbench/{};
        make X86;
        '''.format(bm),
        typ = 'binary',
        name = bm,
        cwd = 'microbench/{}'.format(bm),
        path =  'microbench/{}/bench.X86'.format(bm),
        inputs = [experiments_repo,],
        documentation = 'microbenchmark ({}) binary for X86 ISA'.format(bm)
        )

    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                run = gem5Run.createSERun(
                    'microbench_tests',
                    'gem5/build/X86/gem5.opt',
                    'configs-micro-tests/run_micro.py',
                    'results/X86/run_micro/{}/{}/{}'.format(bm,cpu,mem),
                    gem5_binary,gem5_repo,experiments_repo,
                    cpu,mem,os.path.join('microbench',bm,'bench.X86'))
                run_gem5_instance.apply_async((run, os.getcwd()))
