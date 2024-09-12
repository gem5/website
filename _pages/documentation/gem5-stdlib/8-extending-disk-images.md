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

   Obtain the base disk image from gem5 Resources. Links to the base images are available for [x86](https://resources.gem5.org/resources/x86-ubuntu-24.04-img), [ARM](https://resources.gem5.org/resources/arm-ubuntu-24.04-img), and [RISC-V](https://resources.gem5.org/resources/riscv-ubuntu-24.04-img). Download the image from the `versions` tab.

2. **Unzip the Downloaded Image**

   Unzip the downloaded image using `gunzip`:

   ```sh
   gunzip /path/to/image
   ```

3. **Calculate the `sha256sum` of the Unzipped Image**

   Calculate the `sha256sum` of the unzipped image:

   ```sh
   sha256sum /path/to/unzipped/image
   ```

4. **Create a Packer Script**

   Write a Packer script to use the above disk image as a base image and extend it. Below is an example Packer script with placeholders:

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
     default = "12345" # Update if different for the base image
   }

   variable "ssh_username" {
     type    = string
     default = "gem5" # Update if different for the base image
   }

   source "qemu" "initialize" {
     accelerator      = "kvm"
     boot_command     = [
       "<wait120>",
       "gem5<enter><wait>",
       "12345<enter><wait>",
       "sudo mv /etc/netplan/50-cloud-init.yaml.bak /etc/netplan/50-cloud-init.yaml<enter><wait>",
       "12345<enter><wait>",
       "sudo netplan apply<enter><wait>",
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

**Note:** If you want to view the terminal of the image during the build process, you can use a VNC viewer. Packer will provide a VNC port during the build, which you can connect to using a VNC viewer.

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

## Running disk images in gem5

As these disk iamges throw m5 exit events, we need to handle those to succesfully run the image to boot.

## What are Exit Events?

In gem5, exit events are a way to exit the simulation loop. Exit events can be used to perform operations outside the simulation when triggered, such as resetting stats, switching CPU types, dumping stats, taking checkpoints, etc. By default, the simulation will exit when an exit event is triggered, but we can modify this behavior by writing our own exit event handlers.

## Writing Custom Exit Event Handlers

gem5 expects exit event handlers to be generators, and we can override them by passing our custom generator to the `simulator` object. Let’s say we have a resource that throws an `m5 exit` at some point during execution. Instead of stopping and exiting the simulation, we want to switch processors (assuming we are using the `SimpleSwitchableProcessor`). To do this, we would need to import `ExitEvent` from `gem5.simulate.exit_event`:

```python
from gem5.simulate.exit_event import ExitEvent
```

Now, let's write our handler:

```python
def exit_event_handler():
    # Switch the CPU type
    print("Switching CPU types")
    processor.switch()
    yield False  # Continue the simulation
```

This handler will print a message and switch CPU types. We yield `False` because we want the simulation to continue.

To add our handler to the `simulator` object, we do the following:

```python
simulator = Simulator(
    board=board,
    on_exit_event={
        # Override the default behavior for the first m5 exit event
        ExitEvent.EXIT: exit_event_handler()
    },
)
```

**NOTE:** We pass a call to our handler (`exit_event_handler()`) and not the handler itself (`exit_event_handler`) to the simulator.

## Exit Events Thrown by the New Disk Images

The new disk images on gem5 Resources generate various exit events, such as `m5 exit`, `m5 workbegin`, and `m5 workend` at different stages of the boot process. The generic Ubuntu disk images, like [x86-ubuntu-22.04-img](https://resources.gem5.org/resources/x86-ubuntu-22.04-img?version=1.0.0), [arm-ubuntu-22.04-img](https://resources.gem5.org/resources/arm-ubuntu-22.04-img?version=1.0.0), [riscv-ubuntu-22.04-img](https://resources.gem5.org/resources/riscv-ubuntu-22.04-img?version=1.0.0), [x86-ubuntu-24.04-img](https://resources.gem5.org/resources/x86-ubuntu-24.04-img?version=2.0.0), [arm-ubuntu-24.04-img](https://resources.gem5.org/resources/arm-ubuntu-24.04-img?version=2.0.0), and [riscv-ubuntu-24.04-img](https://resources.gem5.org/resources/riscv-ubuntu-24.04-img?version=1.0.0), trigger three `m5 exit` events, which occur at the following points:

- When the kernel is booted and `sbin/init` is executed.
- After systemd has started, and the `after-boot.sh` script is executed. The `after-boot.sh` script either runs a script passed via `readfile` or drops to an interactive shell if the kernel argument `interactive=true` is set.
- At the end of the `after-boot.sh` script, after running the `readfile` script (if provided). If no script is provided, only the exit is triggered.

All new disk images made after Ubuntu 22.04 on gem5 Resources will also throw these exit events. These disk images have corresponding boot workloads available on gem5 Resources.

In contrast, images like [x86-ubuntu-24.04-npb-img](https://resources.gem5.org/resources/x86-ubuntu-24.04-npb-img?version=2.0.0) and [arm-ubuntu-24.04-npb-img](https://resources.gem5.org/resources/arm-ubuntu-24.04-npb-img?version=2.0.0) generate the same three `m5 exit` events, but they also trigger `m5 workbegin` and `m5 workend` events at the start and end of the Region of Interest (ROI) in the benchmarks being run. The benchmark suites can be found on gem5 Resources at [x86-ubuntu-24.04-npb-suite](https://resources.gem5.org/resources/x86-ubuntu-24.04-npb-suite?version=1.0.0) and [arm-ubuntu-24.04-npb-suite](https://resources.gem5.org/resources/arm-ubuntu-24.04-npb-suite?version=1.0.0).

## Handling Exit Events Thrown by the Disk Images

To fully boot the above disk images, we need to write an exit event handler to prevent the simulation from ending after the first exit (when the kernel is booted). An example exit event handler that we can use with these disk images would look like this:

```python
def exit_event_handler():
    print("First exit: kernel booted")
    yield False  # gem5 is now executing systemd startup
    print("Second exit: Started `after_boot.sh` script")
    # Switch to Timing CPU before running the script
    print("Switching to Timing CPU")
    processor.switch()
    yield False  # gem5 is now executing the `after_boot.sh` script
    print("Third exit: Finished `after_boot.sh` script")
    yield True  # Simulation ends
```

Here, we yield `False` until the `readfile` script has run. We also switch processors (assuming we are using the `SimpleSwitchableProcessor`) after the second exit event.

If using the NPB disk images, we must also handle the `m5 workbegin` and `m5 workend` exit events. A handler for those two events would look like this:

```python
def handle_workbegin():
    print("Resetting stats at the start of ROI!")
    m5.stats.reset()
    yield False

def handle_workend():
    print("Dumping stats at the end of ROI!")
    m5.stats.dump()
    yield False
```

These simple handlers reset stats on `workbegin` and dump stats on `workend`. To add all three handlers to the `simulator`, we can use the following:

```python
simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
        ExitEvent.EXIT: exit_event_handler(),
    },
)
```

The above handlers provide examples of how to handle exit events, allowing the disk image to fully boot and run a `readfile` script.
