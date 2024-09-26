---

layout: documentation  
title: Extending Pre-Built Disk Images Using Packer  
parent: gem5-standard-library  
doc: gem5 documentation  
permalink: /documentation/gem5-stdlib/extending-disk-images  
author: Harshil Patel  

---

gem5 Resources provides pre-built generic Ubuntu 24.04 disk images that you can extend and modify using Packer.

### Steps

1. **Download the Base Disk Image**

   Obtain the base disk image from gem5 Resources.
   These disk images are used to run x86, ARM, and RISC-V simulations in gem5 and are not related to the host system ISA.
   Links to the base images are available for [x86](https://resources.gem5.org/resources/x86-ubuntu-24.04-img), [ARM](https://resources.gem5.org/resources/arm-ubuntu-24.04-img), and [RISC-V](https://resources.gem5.org/resources/riscv-ubuntu-24.04-img). Download the image from the `versions` tab.

2. **Unzip the Downloaded Image**

   Unzip the downloaded image using `gunzip`:

   ```sh
   gunzip /path/to/image
   ```

3. **Calculate the `sha256sum` of the Unzipped Image**

   Packer requires the sha256sum of the base image we are using as a field called `iso_checksum`.
   Calculate the `sha256sum` of the unzipped image:

   ```sh
   sha256sum /path/to/unzipped/image
   ```

4. **Create a Packer Script**

   We use packer to automate the process of creating a disk image.
   Packer used qemu to make the disk.
   It will make the disk image and boot it with the arguments provided.
   It then connects to the image via ssh and runs any commands or instructions it is provided.
   Below is an example Packer script that extends a base image with placeholders:

   ```hcl
   packer {
     required_plugins {
       qemu = {
         source  = "github.com/hashicorp/qemu"
         version = "~> 1"
       }
     }
   }

   variable "image_name" {
     type    = string
     default = "x86-ubuntu-24-04" # Update with your desired image name
   }

   variable "ssh_password" {
     type    = string
     default = "12345" # Update if different for the base image, all 22.04 and 24.04 images on gem5 resources have this password
   }

   variable "ssh_username" {
     type    = string
     default = "gem5" # Update if different for the base image, all 22.04 and 24.04 images on gem5 resources have this username
   }

   source "qemu" "initialize" {
     accelerator      = "kvm"
     boot_command     = [
       "<wait120>", // waiting for the disk image to boot, this will vary depending the host system building the image
       "gem5<enter><wait>", // loging in
       "12345<enter><wait>", // loging in
       "sudo mv /etc/netplan/50-cloud-init.yaml.bak /etc/netplan/50-cloud-init.yaml<enter><wait>", // re enable network as it is disabled by default
       "12345<enter><wait>", // password for sudo
       "sudo netplan apply<enter><wait>", // applying netplan changes
       "<wait>"
     ] # This boot command logs in and re-enables the network so that Packer can connect via SSH
     cpus             = "4"
     disk_size        = "5000"
     format           = "raw"
     headless         = "true"
     disk_image       = "true"
     iso_checksum     = "sha256:# sha256sum of the base image"
     iso_urls         = [""] # Path to the base image
     memory           = "8192"
     output_directory = "" # Output directory path
     qemu_binary      = "/usr/bin/qemu-system-x86_64"
     qemuargs         = [["-cpu", "host"], ["-display", "none"]]
     shutdown_command = "echo '${var.ssh_password}'|sudo -S shutdown -P now"
     ssh_password     = "${var.ssh_password}"
     ssh_username     = "${var.ssh_username}"
     ssh_wait_timeout = "60m"
     vm_name          = "${var.image_name}"
     ssh_handshake_attempts = "1000"
   }

   build {
     sources = ["source.qemu.initialize"]

     provisioner "file" { # You can use this provisioner if you want to transfer files from your host machine to the disk image
       source      = "# path to the file that you want to put on the disk image"
       destination = "# path (on the disk image) where you want to put the file"
     }

     provisioner "shell" {
       execute_command = "echo '${var.ssh_password}' | {{ .Vars }} sudo -E -S bash '{{ .Path }}'"
       scripts         = ["# path to the post-install script that will extend the disk image"]
       expect_disconnect = true
     }
   }
   ```

   After modifying the above Packer script with the necessary information, you can run the Packer file.

5. **Run the Packer File**

   To run the Packer file, use the following commands:

   ```sh
   sudo apt-get update && sudo apt-get install packer # Installing Packer

   packer init /path/to/packer/script
   packer build /path/to/packer/script
   ```

**Note:** If you want to view the terminal output of the disk image during the build process, you can use a VNC viewer. Packer will provide a VNC port during the build, which you can connect to using a VNC viewer.

## Important Notes

- If you are extending the RISC-V base image, please note that you would need to remount the file system as read/write upon logging in before enabling network.
The reason we need to do this is because qemu cant not handle `m5 exit` during the boot process properly so it boots into read only for safety.
The boot command will look something like this:

```hcl
 boot_command =["<wait45>",
                "gem5<enter><wait>",
                "12345<enter><wait>",
                "sudo mount -o remount,rw /<enter><wait>", // remounting file system
                "12345<enter><wait>",
                "sudo mv /etc/netplan/50-cloud-init.yaml.bak /etc/netplan/50-cloud-init.yaml<enter><wait>",
                "sudo netplan apply<enter><wait>",
                "<wait>"
              ]
```
