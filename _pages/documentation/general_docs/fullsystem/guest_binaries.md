---
layout: toc
title: "Guest Binaries"
permalink: /documentation/general_docs/fullsystem/guest_binaries
author: Giacomo Travaglini
---
* TOC
{:toc}

We provide a set of useful prebuilt binaries users can download (in case they don't want to
recompile them from scratch).

There are two ways of downloading them:

* Via Manual Download
* Via Google Cloud Utilities

## Manual Download

Here follows a list of prebuilt binaries to be downloaded by just clicking the link:

### Arm FS Binaries

##### Latest Linux Kernel Image / Bootloader (**recommended**)

The tarball below contains a set of binaries: the Linux kernel and a set of bootloaders

* <http://dist.gem5.org/dist/current/arm/aarch-system-201901106.tar.bz2>

##### Latest Linux Disk Images (**recommended**)

* <http://dist.gem5.org/dist/current/arm/disks/aarch64-ubuntu-trusty-headless.img.bz2>
* <http://dist.gem5.org/dist/current/arm/disks/aarch32-ubuntu-natty-headless.img.bz2>
* <http://dist.gem5.org/dist/current/arm/disks/linaro-minimal-aarch64.img.bz2>
* <http://dist.gem5.org/dist/current/arm/disks/linux-aarch32-ael.img.bz2>

##### Old Linux Kernel/Disk Image

These images are not supported. If you run into problems, we will do our best to help, but there is no guarantee these will work with the latest gem5 version

* <http://dist.gem5.org/dist/current/arm/aarch-system-20170616.tar.xz>
* <http://dist.gem5.org/dist/current/arm/aarch-system-20180409.tar.xz>
* <http://dist.gem5.org/dist/current/arm/arm-system-dacapo-2011-08.tgz>
* <http://dist.gem5.org/dist/current/arm/arm-system.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/arm64-system-02-2014.tgz>
* <http://dist.gem5.org/dist/current/arm/kitkat-overlay.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/linux-arm-arch.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/vmlinux-emm-pcie-3.3.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/vmlinux.arm.smp.fb.3.2.tar.gz>

## Google Cloud Utilities (gsutil)

gsutil is a Python application that lets you access Cloud Storage from the command line.
Please have a look at the following documentation which will guide you through the process
of installing the utility

* [gsutil tool](https://cloud.google.com/storage/docs/gsutil)

Once installed (NOTE: It require you to provide a valid google account) it will be possible to inspect/download gem5 binaries via the following command line.

```
gsutil cp -r gs://dist.gem5.org/dist/<binary>
```

