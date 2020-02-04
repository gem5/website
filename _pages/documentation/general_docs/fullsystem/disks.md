---
layout: documentation
title: Creating disk images
doc: gem5 documentation
parent: fullsystem
permalink: documentation/general_docs/fullsystem/disks
---

# Creating disk images for full system mode

In full-system mode, gem5 relies on a disk image with an installed operating system to run simulations.
A disk device in gem5 gets its initial contents from disk image.
The disk image file stores all the bytes present on the disk just as you would find them on an actual device.
Some other systems also use disk images which are in more complicated formats and which provide compression, encryption, etc. gem5 currently only supports raw images, so if you have an image in one of those other formats, you'll have to convert it into a raw image before you can use it in a simulation.
There are often tools available which can convert between the different formats.

There are multiple ways of creating a disk image which can be used with gem5.
Following are four different methods to build disk images:

- Using gem5 utils to create a disk image
- Using gem5 utils and chroot to create a disk image
- Using QEMU to create a disk image
- Using Packer to create a disk image

All of these methods are independent of each other.
Next, we will discuss each of these methods one by one.

## 1) Using gem5 utils to create a disk image

```md
Disclaimer: This is from the old website and some of the stuff in this method can be out-dated.

```
Because a disk image represents all the bytes on the disk itself, it contains more than just a file system.
For hard drives on most systems, the image starts with a partition table.
Each of the partitions in the table (frequently only one) is also in the image.
If you want to manipulate the entire disk you'll use the entire image, but if you want to work with just one partition and/or the file system on it, you'll need to specifically select that part of the image.
The losetup command (discussed below) has a -o option which lets you specify where to start in an image.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Oh3NK12fnbg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><div class='thumbcaption'>A youtube video of working with image files using qemu on Ubuntu 12.04 64bit. Video resolution can be set to 1080</div>


### Creating an empty image

You can use the ./util/gem5img.py script provided with gem5 to build the disk image.
It's a good idea to understand how to build an image in case something goes wrong or you need to do something in an unusual way.
However, in this mehtod, we are using gem5img.py script to go through the process of building and formatting an image.
If you want to understand the guts of what it's doing see below.
Running gem5img.py may require you to enter the sudo password.
*You should never run commands as the root user that you don't understand! You should look at the file util/gem5img.py and ensure that it isn't going to do anything malicious to your computer!*

You can use the "init" option with gem5img.py to create an empty image, "new", "partition", or "format" to perform those parts of init independently, and "mount" or "umount" to mount or unmount an existing image.

### Mounting an image

To mount a file system on your image file, first find a loopback device and attach it to your image with an appropriate offset as will be described further in the [Formatting](#formatting) section.

```sh
mount -o loop,offset=32256 foo.img
```

<iframe width="560" height="315" src="https://www.youtube.com/embed/OXH1oxQbuHA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><div class='thumbcaption'>A youtube video of add file using mount on Ubuntu 12.04 64bit. Video resolution can be set to 1080</div>

### Unmounting

To unmount an image, use the umount command like you normally would.

```sh
umount
```

### Image Contents

Now that you can create an image file and mount it's file system, you'll want to actually put some files in it.
You're free to use whatever files you want, but the gem5 developers have found that Gentoo stage3 tarballs are a great starting point.
They're essentially an almost bootable and fairly minimal Linux installation and are available for a number of architectures.

If you choose to use a Gentoo tarball, first extract it into your mounted image.
The /etc/fstab file will have placeholder entries for the root, boot, and swap devices.
You'll want to update this file as apporpriate, deleting any entries you aren't going to use (the boot partition, for instance).
Next, you'll want to modify the inittab file so that it uses the m5 utility program (described elsewhere) to read in the init script provided by the host machine and to run that.
If you allow the normal init scripts to run, the workload you're interested in may take much longer to get started, you'll have no way to inject your own init script to dynamically control what benchmarks are started, for instance, and you'll have to interact with the simulation through a simulated terminal which introduces non-determinism.

#### Modifications

By default gem5 does not store modifications to the disk back to the underlying image file.
Any changes you make will be stored in an intermediate COW layer and thrown away at the end of the simulation.
You can turn off the COW layer if you want to modify the underlying disk.

#### Kernel and bootloader

Also, generally speaking, gem5 skips over the bootloader portion of boot and loads the kernel into simulated memory itself. This means that there's no need to install a bootloader like grub to your disk image, and that you don't have to put the kernel you're going to boot from on the image either.
The kernel is provided separately and can be changed out easily without having to modify the disk image.

### Manipulating images with loopback devices

#### Loopback devices

Linux supports loopback devices which are devices backed by files.
By attaching one of these to your disk image, you can use standard Linux commands on it which normally run on real disk devices.
You can use the mount command with the "loop" option to set up a loopback device and mount it somewhere.
Unfortunately you can't specify an offset into the image, so that would only be useful for a file system image, not a disk image which is what you need.
You can, however, use the lower level losetup command to set up a loopback device yourself and supply the proper offset.
Once you've done that, you can use the mount command on it like you would on a disk partition, format it, etc.
If you don't supply an offset the loopback device will refer to the whole image, and you can use your favorite program to set up the partitions on it.

### Working with image files

To create an empty image from scratch, you'll need to create the file itself, partition it, and format (one of) the partition(s) with a file system.

####  Create the actual file

First, decide how large you want your image to be.
It's a good idea to make it large enough to hold everything you know you'll need on it, plus some breathing room.
If you find out later it's too small, you'll have to create a new larger image and move everything over.
If you make it too big, you'll take up actual disk space unnecessarily and make the image harder to work with.
Once you've decided on a size you'll want to actually create the file.
Basically, all you need to do is create a file of a certain size that's full of zeros.
One approach is to use the dd command to copy the right number of bytes from /dev/zero into the new file.
Alternatively you could create the file, seek in it to the last byte, and write one zero byte.
All of the space you skipped over will become part of the file and is defined to read as zeroes, but because you didn't explicitly write any data there, most file systems are smart enough to not actually store that to disk.
You can create a large image that way but take up very little space on your physical disk.
Once you start writing to the file later that will change, and also if you're not careful, copying the file may expand it to its full size.

#### Partitioning

First, find an available loopback device using the losetup command with the -f option.

```sh
losetup -f
```

Next, use losetup to attach that device to your image.
If the available device was /dev/loop0 and your image is foo.img, you would use a command like this.

```sh
losetup /dev/loop0 foo.img
```

/dev/loop0 (or whatever other device you're using) will now refer to your entire image file.
Use whatever partitioning program you like on it to set up one (or more) paritions.
For simplicity it's probably a good idea to create only one parition that takes up the entire image.
We say it takes up the entire image, but really it takes up all the space except for the partition table itself at the beginning of the file, and possibly some wasted space after that for DOS/bootloader compatibility.

From now on we'll want to work with the new partition we created and not the whole disk, so we'll free up the loopback device using losetup's -d option

```sh
losetup -d /dev/loop0
```

#### Formatting

First, find an available loopback device like we did in the partitioning step above using losetup's -f option.

```sh
losetup -f
```

We'll attach our image to that device again, but this time we only want to refer to the partition we're going to put a file system on.
For PC and Alpha systems, that partition will typically be one track in, where one track is 63 sectors and each sector is 512 bytes, or 63 * 512 = 32256 bytes.
The correct value for you may be different, depending on the geometry and layout of your image.
In any case, you should set up the loopback device with the -o option so that it represents the partition you're interested in.

```sh
losetup -o 32256 /dev/loop0 foo.img
```

Next, use an appropriate formating command, often mke2fs, to put a file system on the partition.

```sh
mke2fs /dev/loop0
```

You've now successfully created an empty image file.
You can leave the loopback device attached to it if you intend to keep working with it (likely since it's still empty) or clean it up using losetup -d.

```sh
losetup -d /dev/loop0
```

Don't forget to clean up the loopback device attached to your image with the losetup -d command.

```sh
losetup -d /dev/loop0
```

## 2) Using gem5 utils and chroot to create a disk image

The discussion in this section assumes that you have already checked out a version of gem5 and can build and run gem5 in full-system mode.
We will use the x86 ISA for gem5 in this discussion, and this is mostly applicable to other ISAs as well.

### Creating a blank disk image

The first step is to create a blank disk image (usually a .img file).
This is similar to what we did in the first metod.
We can use the gem5img.py script provided by gem5 developers.
To create a blank disk image, which is formatted with ext2 by default, simply run the following.

```
> util/gem5img.py init ubuntu-14.04.img 4096
```

This command creates a new image, called "ubuntu-14.04.img" that is 4096 MB.
This command may require you to enter the sudo password, if you don't have permission to create loopback devices.
*You should never run commands as the root user that you don't understand! You should look at the file util/gem5img.py and ensure that it isn't going to do anything malicious to your computer!*

We will be using util/gem5img.py heavily throughout this section, so you may want to understand it better.
If you just run `util/gem5img.py`, it displays all of the possible commands.

```
Usage: %s [command] <command arguments>
where [command] is one of
    init: Create an image with an empty file system.
    mount: Mount the first partition in the disk image.
    umount: Unmount the first partition in the disk image.
    new: File creation part of "init".
    partition: Partition part of "init".
    format: Formatting part of "init".
Watch for orphaned loopback devices and delete them with
losetup -d. Mounted images will belong to root, so you may need
to use sudo to modify their contents
```

### Copying root files to the disk

Now that we have created a blank disk, we need to populate it with all of the OS files.
Ubuntu distributes a set of files explicitly for this purpose.
You can find the [Ubuntu core](https://wiki.ubuntu.com/Core) distribution for 14.04 at <http://cdimage.ubuntu.com/releases/14.04/release/>. Since we are simulating an x86 machine, we will use `ubuntu-core-14.04-core-amd64.tar.gz`.
Download whatever image is appropriate for the system you are simulating.

Next, we need to mount the blank disk and copy all of the files onto the disk.

```
mkdir mnt
../../util/gem5img.py mount ubuntu-14.04.img mnt
wget http://cdimage.ubuntu.com/ubuntu-core/releases/14.04/release/ubuntu-core-14.04-core-amd64.tar.gz
sudo tar xzvf ubuntu-core-14.04-core-amd64.tar.gz -C mnt
```

The next step is to copy a few required files from your working system onto the disk so we can chroot into the new disk. We need to copy `/etc/resolv.conf` onto the new disk.

```
sudo cp /etc/resolv.conf mnt/etc/
```

### Setting up gem5-specific files

#### Create a serial terminal

By default, gem5 uses the serial port to allow communication from the host system to the simulated system. To use this, we need to create a serial tty.
Since Ubuntu uses upstart to control the init process, we need to add a file to /etc/init which will initialize our terminal.
Also, in this file, we will add some code to detect if there was a script passed to the simulated system.
If there is a script, we will execute the script instead of creating a terminal.

Put the following code into a file called /etc/init/tty-gem5.conf

```
# ttyS0 - getty
#
# This service maintains a getty on ttyS0 from the point the system is
# started until it is shut down again, unless there is a script passed to gem5.
# If there is a script, the script is executed then simulation is stopped.

start on stopped rc RUNLEVEL=[12345]
stop on runlevel [!12345]

console owner
respawn
script
   # Create the serial tty if it doesn't already exist
   if [ ! -c /dev/ttyS0 ]
   then
      mknod /dev/ttyS0 -m 660 /dev/ttyS0 c 4 64
   fi

   # Try to read in the script from the host system
   /sbin/m5 readfile > /tmp/script
   chmod 755 /tmp/script
   if [ -s /tmp/script ]
   then
      # If there is a script, execute the script and then exit the simulation
      exec su root -c '/tmp/script' # gives script full privileges as root user in multi-user mode
      /sbin/m5 exit
   else
      # If there is no script, login the root user and drop to a console
      # Use m5term to connect to this console
      exec /sbin/getty --autologin root -8 38400 ttyS0
   fi
end script
```

#### Setup localhost

We also need to set up the localhost loopback device if we are going to use any applications that use it.
To do this, we need to add the following to the `/etc/hosts` file.

```
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

#### Update fstab

Next, we need to create an entry in `/etc/fstab` for each partition we want to be able to access from the simulated system. Only one partition is absolutely required (`/`); however, you may want to add additional partitions, like a swap partition.

The following should appear in the file `/etc/fstab`.

```
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system>    <mount point>   <type>  <options>   <dump>  <pass>
/dev/hda1      /       ext3        noatime     0 1
```

#### Copy the `m5` binary to the disk

gem5 comes with an extra binary application that executes pseudo-instructions to allow the simulated system to interact with the host system.
To build this binary, run `make -f Makefile.<isa>` in the `gem5/m5` directory, where `<isa>` is the ISA that you are simulating (e.g., x86). After this, you should have an `m5` binary file.
Copy this file to /sbin on your newly created disk.

After updating the disk with all of the gem5-specific files, unless you are going on to add more applications or copying additional files, unmount the disk image.

```
> util/gem5img.py umount mnt
```

### Install new applications

The easiest way to install new applications on to your disk, is to use `chroot`.
This program logically changes the root directory ("/") to a different directory, mnt in this case.
Before you can change the root, you first have to set up the special directories in your new root. To do
this, we use `mount -o bind`.

```
> sudo /bin/mount -o bind /sys mnt/sys
> sudo /bin/mount -o bind /dev mnt/dev
> sudo /bin/mount -o bind /proc mnt/proc
```

After binding those directories, you can now `chroot`:

```
> sudo /usr/sbin/chroot mnt /bin/bash
```

At this point you will see a root prompt and you will be in the `/`
directory of your new disk.

You should update your repository information.

```
> apt-get update
```

You may want to add the universe repositories to your list with the
following commands.
Note: The first command is require in 14.04.

```
> apt-get install software-properties-common
> add-apt-repository universe
> apt-get update
```

Now, you are able to install any applications you could install on a
native Ubuntu machine via `apt-get`.

Remember, after you exit you need to unmount all of the directories we
used bind on.

```
> sudo /bin/umount mnt/sys
> sudo /bin/umount mnt/proc
> sudo /bin/umount mnt/dev
```


## 3) Using QEMU to create a disk image

This method is a follow-up on the previous method to create a disk image.
We will see how to create, edit and set up a disk image using qemu instead of relying on gem5 tools.
This section assumes that you have installed qemu on your system.
In Ubuntu, this can be done with

```
sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
```

### Step 1: Create an empty disk
Using the qemu disk tools, create a blank raw disk image.
In this case, I chose to create a disk named "ubuntu-test.img" that is 8GB.

```
qemu-img create ubuntu-test.img 8G
```

### Step 2: Install ubuntu with qemu
Now that we have a blank disk, we are going to use qemu to install Ubuntu on the disk.
It is encouraged that you use the server version of Ubuntu since gem5 does not have great support for displays.
Thus, the desktop environment isn't very useful.

First, you need to download the installation CD image from the [Ubuntu website](https://www.ubuntu.com/download/server).

Next, use qemu to boot off of the CD image, and set the disk in the system to be the blank disk you created above.
Ubuntu needs at least 1GB of memory to install correctly, so be sure to configure qemu to use at least 1GB memory.

```
qemu-system-x86_64 -hda ../gem5-fs-testing/ubuntu-test.img -cdrom ubuntu-16.04.1-server-amd64.iso -m 1024 -enable-kvm -boot d
```

With this, you can simply follow the on-screen directions to install Ubuntu to the disk image.
The only gotcha in the installation is that gem5's IDE drivers don't seem to play nicely with logical paritions.
Thus, during the Ubuntu install, be sure to manually partition the disk and remove any logical partitions.
You don't need any swap space on the disk anyway, unless you're doing something specifically with swap space.

### Step 3: Boot up and install needed software

Once you have installed Ubuntu on the disk, quit qemu and remove the `-boot d` option so that you are not booting off of the CD anymore.
Now, you can again boot off of the main disk image you have installed Ubuntu on.

Since we're using qemu, you should have a network connection (although [ping won't
work](http://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29)).
When booting in qemu, you can just use `sudo apt-get install` and
install any software you need on your disk.

```
qemu-system-x86_64 -hda ../gem5-fs-testing/ubuntu-test.img -cdrom ubuntu-16.04.1-server-amd64.iso -m 1024 -enable-kvm
```

### Step 4: Update init script

By default, gem5 expects a modified init script which loads a script off of the host to execute in the guest.
To use this feature, you need to follow the steps below.

Alternatively, you can install the precompiled binaries for x86 found on this [website](http://cs.wisc.edu/~powerjg/files/gem5-guest-tools-x86.tgz).
From qemu, you can run the following, which completes the above steps for you.

```
wget http://cs.wisc.edu/~powerjg/files/gem5-guest-tools-x86.tgz
tar xzvf gem5-guest-tools-x86.tgz
cd gem5-guest-tools/
sudo ./install
```

Now, you can use the `system.readfile` parameter in your Python config scripts. This file will automatically be loaded (by the `gem5init` script) and executed.

### Manually installing the gem5 init script

First, build the m5 binary on the host.

```
cd util/m5
make -f Makefile.x86
```

Then, copy this binary to the guest and put it in `/sbin`. Also, create a link from `/sbin/gem5`.

Then, to get the init script to execute when gem5 boots, create file /lib/systemd/system/gem5.service with the following:

```
[Unit]
Description=gem5 init script
Documentation=http://gem5.org
After=getty.target

[Service]
Type=idle
ExecStart=/sbin/gem5init
StandardOutput=tty
StandardInput=tty-force
StandardError=tty

[Install]
WantedBy=default.target
```

Enable the gem5 service and disable the ttyS0 service.

```
systemctl enable gem5.service
```

Finally, create the init script that is executed by the service. In
`/sbin/gem5init`:

```
#!/bin/bash -

CPU=`cat /proc/cpuinfo | grep vendor_id | head -n 1 | cut -d ' ' -f2-`
echo "Got CPU type: $CPU"

if [ "$CPU" != "M5 Simulator" ];
then
    echo "Not in gem5. Not loading script"
    exit 0
fi

# Try to read in the script from the host system
/sbin/m5 readfile > /tmp/script
chmod 755 /tmp/script
if [ -s /tmp/script ]
then
    # If there is a script, execute the script and then exit the simulation
    su root -c '/tmp/script' # gives script full privileges as root user in multi-user mode
    sync
    sleep 10
    /sbin/m5 exit
fi
echo "No script found"
```

### Problems and (some) solutions

You might run into some problems while following this method.
Some of the issues and solutions are discussed on this [page](http://www.lowepower.com/jason/setting-up-gem5-full-system.html).

## 4) Using Packer to create a disk image

This section discusses an automated way of creating gem5-compatible disk images with Ubuntu server installed. We make use of packer to do this which makes use of a .json template file to build and configure a disk image. The template file could be configured to build a disk image with specific benchmarks installed. The mentioned template file can be found [here](/assets/files/packer_template.json).


### Building a Simple Disk Image with Packer

#### a. How It Works, Briefly
We use [Packer](https://www.packer.io/) and [QEMU](https://www.qemu.org/) to automate the process of disk creation.
Essentially, QEMU is responsible for setting up a virtual machine and all interactions with the disk image during the building process.
The interactions include installing Ubuntu Server to the disk image, copying files from your machine to the disk image, and running scripts on the disk image after Ubuntu is installed.
However, we will not use QEMU directly.
Packer provides a simpler way to interact with QEMU using a JSON script, which is more expressive than using QEMU from command line.

#### b. Install Required Software/Dependencies
If not already installed, QEMU can be installed using:
```shell
sudo apt-get install qemu
```
Download the Packer binary from [the official website](https://www.packer.io/downloads.html).

#### c. Customize the Packer Script
The default packer script `template.json` should be modified and adapted according to the required disk image and the avaiable resources for the build proces. We will rename the default template to `[disk-name].json`. The variables that should be modified appear at the end of `[disk-name].json` file, in `variables` section.
The configuration files that are used to build the disk image, and the directory structure is shown below:
```shell
disk-image/
    [disk-name].json: packer script
    Any experiment-specific post installation script
    post-installation.sh: generic shell script that is executed after Ubuntu is installed
    preseed.cfg: preseeded configuration to install Ubuntu
```

##### i. Customizing the VM (Virtual Machine)
In `[disk-name].json`, following variables are available to customize the VM:

| Variable         | Purpose     | Example  |
| ---------------- |-------------|----------|
| [vm_cpus](https://www.packer.io/docs/builders/qemu.html#cpus) **(should be modified)** | number of host CPUs used by VM | "2": 2 CPUs are used by the VM |
| [vm_memory](https://www.packer.io/docs/builders/qemu.html#memory) **(should be modified)**| amount of VM memory, in MB | "2048": 2 GB of RAM are used by the VM |
| [vm_accelerator](https://www.packer.io/docs/builders/qemu.html#accelerator) **(should be modified)** | accelerator used by the VM e.g. Kvm | "kvm": kvm will be used |

<br />

##### ii. Customizing the Disk Image
In `[disk-name].json`, disk image size can be customized using following variable:

| Variable        | Purpose     | Example  |
| ---------------- |-------------|----------|
| [image_size](https://www.packer.io/docs/builders/qemu.html#disk_size) **(should be modified)** | size of the disk image, in megabytes | "8192": the image has the size of 8 GB  |
| [image_name] | name of the built disk image | "boot-exit"  |

<br />

##### iii. File Transfer
While building a disk image, users would need to move their files (benchmarks, data sets etc.) to
the disk image. In order to do this file transfer, in `[disk-name].json` under `provisioners`, you could add the following:

```shell
{
    "type": "file",
    "source": "post_installation.sh",
    "destination": "/home/gem5/",
    "direction": "upload"
}
```
The above example copies the file `post_installation.sh` from the host to `/home/gem5/` in the disk image.
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

##### iv. Install Benchmark Dependencies
To install the dependencies, you can use a bash script `post_installation.sh`, which will be run after the Ubuntu installation and file copying is done.
For example, if we want to install `gfortran`, add the following in `post_installation.sh`:
```shell
echo '12345' | sudo apt-get install gfortran;
```
In the above example, we assume that the user password is `12345`.
This is essentially a bash script that is executed on the VM after the file copying is done, you could modify the script as a bash script to fit any purpose.

##### v. Running Other Scripts on Disk Image
In `[disk-name].json`, we could add more scripts to `provisioners`.
Note that the files are on the host, but the effects are on the disk image.
For example, the following example runs `post_installation.sh` after Ubuntu is installed,
{% raw %}
```sh
{
    "type": "shell",
    "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
    "scripts":
    [
        "post-installation.sh"
    ]
}
```
{% endraw %}

#### d. Build the Disk Image

##### i. Build
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

##### ii. Inspect the Building Process
While the building of disk image takes place, Packer will run a VNC (Virtual Network Computing) server and you will be able to see the building process by connecting to the VNC server from a VNC client. There are a plenty of choices for VNC client. When you run the Packer script, it will tell you which port is used by the VNC server. For example, if it says `qemu: Connecting to VM via VNC (127.0.0.1:5932)`, the VNC port is 5932.
To connect to VNC server from the VNC client, use the address `127.0.0.1:5932` for a port number 5932.
If you need port forwarding to forward the VNC port from a remote machine to your local machine, use SSH tunneling
```shell
ssh -L 5932:127.0.0.1:5932 <username>@<host>
```
This command will forward port 5932 from the host machine to your machine, and then you will be able to connect to the VNC server using the address `127.0.0.1:5932` from your VNC viewer.

**Note**: While Packer is installing Ubuntu, the terminal screen will display "waiting for SSH" without any update for a long time.
This is not an indicator of whether the Ubuntu installation produces any errors.
Therefore, we strongly recommend using VNC viewer at least once to inspect the image building process.


