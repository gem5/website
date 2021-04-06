---
layout: documentation
title: Disk Images
doc: gem5art
parent: main
permalink: /documentation/gem5art/main/disks
Authors:
  - Hoa Nguyen
  - Ayaz Akram
---

# Disk Images

## Introduction
This section discusses an automated way of creating gem5-compatible disk images with Ubuntu server installed. We make use of [Packer](https://www.packer.io/) which uses .json template files to build and configure a disk image. These template files can be configured to build a disk image with specific benchmarks installed.

## Building a Simple Disk Image with Packer
<a name="packerbriefly"></a>
### a. How It Works, Briefly
We use [Packer](https://www.packer.io/) and [QEMU](https://www.qemu.org/) to automate the process of disk creation.
Essentially, QEMU is responsible for setting up a virtual machine and all interactions with the disk image during the building process.
The interactions include installing Ubuntu Server to the disk image, copying files from your machine to the disk image, and running scripts on the disk image after Ubuntu is installed.
However, we will not use QEMU directly.
Packer provides a simpler way to interact with QEMU using a JSON script, which is more expressive than using QEMU from command line.
<a name="dependencies"></a>
### b. Install Required Software/Dependencies
If not already installed, QEMU can be installed using:
```shell
sudo apt-get install qemu
```
The packer binary can be downloaded from [the official website](https://www.packer.io/downloads.html).
For example, the following command downloads packer version 1.7.2 for Linux platforms,

```sh
wget https://releases.hashicorp.com/packer/1.7.2/packer_1.7.2_linux_amd64.zip
unzip packer_1.7.2_linux_amd64.zip
```

<a name="customizing"></a>
### c. Customize the Packer Script
The default packer script `template.json` should be modified and adapted according to the required disk image and the available resources for the build process. We will rename the default template to `[disk-name].json`. The variables that should be modified appear at the end of `[disk-name].json` file, in `variables` section.
The configuration files that we use to build the disk image, and the directory structure is shown below:
```shell
disk-image/
  experiment-specific-folder/
    [disk-name].json: packer script
    Any experiment-specific post installation script

  shared/
    post-installation.sh: generic shell script that is executed after Ubuntu is installed
    preseed.cfg: pre-seeded configuration to install Ubuntu
```

<a name="customizingVM"></a>
#### i. Customizing the VM (Virtual Machine)
In `[disk-name].json`, following variables are available to customize the VM (to be used for the disk building process):

| Variable         | Purpose     | Example  |
| ---------------- |-------------|----------|
| [vm_cpus](https://www.packer.io/docs/builders/qemu.html#cpus) **(should be modified)** | number of host CPUs used by VM | "2": 2 CPUs are used by the VM |
| [vm_memory](https://www.packer.io/docs/builders/qemu.html#memory) **(should be modified)** | amount of memory used by VM, in megabytes | "2048": 2 GB of RAM are used by the VM |
| [vm_accelerator](https://www.packer.io/docs/builders/qemu.html#accelerator) **(should be modified)** | accelerator used by the VM, e.g. kvm | "kvm": kvm will be used |

<a name="customizingscripts"></a>
#### ii. Customizing the Disk Image
In `[disk-name].json`, disk image size can be customized using following variable:

| Variable        | Purpose     | Example  |
| ---------------- |-------------|----------|
| [image_size](https://www.packer.io/docs/builders/qemu.html#disk_size) **(should be modified)** | size of the disk image, in megabytes | "8192": the image has the size of 8 GB  |
| [image_name] | name of the built disk image | "boot-exit"  |




<a name="customizingscripts2"></a>
#### iii. File Transfer
While building a disk image, users would need to move their files (benchmarks, data sets etc.) to
the disk image. In order to do this file transfer, in `[disk-name].json` under `provisioners`, you could add the following:

```shell
{
    "type": "file",
    "source": "shared/post_installation.sh",
    "destination": "/home/gem5/",
    "direction": "upload"
}
```
The above example copies the file `shared/post_installation.sh` from the host to `/home/gem5/` in the disk image.
This method is also capable of copying a folder from host to the disk image and vice versa.
It is important to note that the trailing slash affects the copying process [(more details)](https://www.packer.io/docs/provisioners/file.html#directory-uploads).
The following are some notable examples of the effect of using slash at the end of the paths.

| `source`        | `destination`     | `direction`  |  `Effect`  |
| ---------------- |-------------|----------|-----|
| `foo.txt` | `/home/gem5/bar.txt` | `upload` | copy file (host) to file (image) |
| `foo.txt` | `bar/` | `upload` | copy file (host) to folder (image) |
| `/foo` | `/tmp` | `upload` | `mkdir /tmp/foo` (image);  `cp -r /foo/* (host) /tmp/foo/ (image)`; |
| `/foo/` | `/tmp` | `upload` | `cp -r /foo/* (host) /tmp/ (image)` |

If `direction` is `download`, the files will be copied from the image to the host.
**Note**: [This is a way to run script once after installing Ubuntu without copying to the disk image](#customizingscripts3).

<a name="customizingscripts3"></a>
#### iv. Install ing Benchmark Dependencies
To install the dependencies, we utilize the bash script `shared/post_installation.sh`, which will be run after the Ubuntu installation and file copying is done.
For example, if we want to install `gfortran`, add the following in `scripts/post_installation.sh`:
```shell
echo '12345' | sudo apt-get install gfortran;
```
In the above example, we assume that the user password is `12345`.
This is essentially a bash script that is executed on the VM after the file copying is done, you could modify the script as a bash script to fit any purpose.
<a name="customizingscripts4"></a>
#### v. Running Other Scripts on Disk Image
In `[disk-name].json`, we could add more scripts to `provisioners`.
Note that the files are on the host, but the effects are on the disk image.
For example, the following example runs `shared/post_installation.sh` after Ubuntu is installed,
```shell
{
    "type": "shell",
    "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
    "scripts":
    [
        "scripts/post-installation.sh"
    ]
}
```
<a name="buildsimple"></a>
### d. Building the Disk Image
<a name="simplebuild"></a>
#### i. Building the Disk Image
In order to build a disk image, the template file is first validated using:
```sh
./packer validate [disk-name].json
```
Then, the template file can be used to build the disk image:
```sh
./packer build [disk-name].json
```

On a fairly recent machine, the building process should not take more than 15 minutes to complete.
The disk image with the user-defined name (image_name) will be produced in a folder called [image_name]-image.
[We recommend to use a VNC viewer in order to inspect the building process](#inspect).
<a name="inspect"></a>
#### ii. Inspecting the Building Process
While the building process of disk image takes place, packer will run a VNC (Virtual Network Computing) server and you will be able to see the building process by connecting to the VNC server from a VNC client. There are a plenty of choices for VNC client. When you run the packer script, it will tell you which port is used by the VNC server. For example, if it says `qemu: Connecting to VM via VNC (127.0.0.1:5932)`, the VNC port is 5932.
To connect to VNC server from the VNC client, use the address `127.0.0.1:5932` for a port number 5932.
If you need port forwarding to forward the VNC port from a remote machine to your local machine, use SSH tunneling
```shell
ssh -L 5932:127.0.0.1:5932 <username>@<host>
```
This command will forward port 5932 from the host machine to your machine, and then you will be able to connect to the VNC server using the address `127.0.0.1:5932` from your VNC viewer.

**Note**: While packer is installing Ubuntu, the terminal screen will display "waiting for SSH" without any update for a long time.
This is not an indicator of whether the Ubuntu installation produces any errors.
Therefore, we strongly recommend using VNC viewer at least once to inspect the image building process.
<a name="checking"></a>

