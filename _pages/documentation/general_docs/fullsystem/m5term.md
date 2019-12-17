---
layout: documentation
title: "m5 term"
doc: gem5 documentation
parent: fullsystem
permalink: /documentation/general_docs/fullsystem/m5term
---
# m5 term
The m5term program allows the user to connect to the simulated console interface that full-system gem5 provides. Simply change into the util/term directory and build m5term:
```
% cd gem5/util/term
% make
gcc  -o m5term term.c
% make install
sudo install -o root -m 555 m5term /usr/local/bin
```
The usage of m5term is:
```
./m5term <host> <port>
```
	<host> is the host that is running gem5

	<port> is the console port to connect to. gem5 defaults to
	using port 3456, but if the port is used, it will try the next
	higher port until it finds one available.

	If there are multiple systems running within one simulation,
	there will be a console for each one.  (The first system's
	console will be on 3456 and the second on 3457 for example)

	m5term uses '~' as an escape character.  If you enter
	the escape character followed by a '.', the m5term program
	will exit.

m5term can be used to interactively work with the simulator, though users must often set various terminal settings to get things to work

A slightly shortened example of m5term in action:

	% m5term localhost 3456
	==== m5 slave console: Console 0 ====
	M5 console
	Got Configuration 127
	memsize 8000000 pages 4000
	First free page after ROM 0xFFFFFC0000018000
	HWRPB 0xFFFFFC0000018000 l1pt 0xFFFFFC0000040000 l2pt 0xFFFFFC0000042000 l3pt_rpb 0xFFFFFC0000044000 l3pt_kernel 0xFFFFFC0000048000 l2reserv 0xFFFFFC0000046000
	CPU Clock at 2000 MHz IntrClockFrequency=1024
	Booting with 1 processor(s)
	...
	...
	VFS: Mounted root (ext2 filesystem) readonly.
	Freeing unused kernel memory: 480k freed
	init started:  BusyBox v1.00-rc2 (2004.11.18-16:22+0000) multi-call binary

	PTXdist-0.7.0 (2004-11-18T11:23:40-0500)

	mounting filesystems...
	EXT2-fs warning: checktime reached, running e2fsck is recommended
	loading script...
	Script from M5 readfile is empty, starting bash shell...
	# ls
	benchmarks  etc         lib         mnt         sbin        usr
	bin         floppy      lost+found  modules     sys         var
	dev         home        man         proc        tmp         z
	#
