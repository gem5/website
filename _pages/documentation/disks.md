---
layout: page
title: Creating disk images
parent: documentation
permalink: documentation/disks/
author: Ayaz Akram
---

In full-system mode, gem5 relies on a disk image with an installed operating system to run simulations.
A disk device in gem5 gets its initial contents from disk image.
The disk image file stores all the bytes present on the disk just as you would find them on an actual device.
Some other systems also use disk images which are in more complicated formats and which provide compression, encryption, etc. gem5 currently only supports raw images, so if you have an image in one of those other formats, you'll have to convert it into a raw image before you can use it in a simulation.
There are often tools available which can convert between the different formats.

There are multiple ways of creating a disk image which can be used with gem5.

## Using gem5 utils to create a disk image

Because a disk image represents all the bytes on the disk itself, it contains more than just a file system.
For hard drives on most systems, the image starts with a partition table.
Each of the partitions in the table (frequently only one) is also in the image.
If you want to manipulate the entire disk you'll use the entire image, but if you want to work with just one partition and/or the file system on it, you'll need to specifically select that part of the image.
The losetup command (discussed below) has a -o option which lets you specify where to start in an image.

## Using QEMU to create a disk image

## Using Packer to create a disk image