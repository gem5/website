---
layout: page
title: Getting Started with gem5
permalink: /getting_started/
author: Jason Lowe-Power
---

# Getting Started with gem5

## First steps

The gem5 simulator is most useful for research when you build new models and new features on top of the current codebase.
Thus, the most common way to use gem5 is to download the source and build it yourself.

To download gem5, you can use [`git`](https://git-scm.com/) to checkout to current stable branch.
If you're not familiar with version control or git, The [git book](https://git-scm.com/book/en/v2) (available online for free) is a great way to learn more about git and become more comfortable using version control.
The canonical version of gem5 is hosted by Google on googlesource.com.
However, there is a [GitHub mirror](https://github.com/gem5/gem5) as well.
It is strongly suggested to use the googlesource version of gem5, and it is required if you want to [contribute any changes](/contributing) back to the gem5 mainline.

```
git clone https://gem5.googlesource.com/public/gem5
```

After cloning the source code, you can build gem5 by using [`scons`](https://scons.org/).
Building gem5 can take anywhere from a few minutes on a large server to 45 minutes on a laptop.
gem5 must be built on a Unix platform.
Linux is tested on every commit, and some people have been able to use MacOS as well, though it is not regularly tested.
It is strongly suggested to *not* try to compile gem5 when running on a virtual machine.
When running with a VM on a laptop gem5 can take over an hour just to compile.
The [building gem5](/documentation/general_docs/building) provides more details on building gem5 and its dependencies.

```
cd gem5
scons build/X86/gem5.opt -j <NUMBER OF CPUs ON YOUR PLATFORM>
```

Now that you have a gem5 binary, you can run your first simulation!
gem5's interface is Python scripts.
The gem5 binary reads in and executes the provided Python script which creates the system under test and executes the simulator.
In this example, the script creates a *very* simple system and executes a "hello world" binary.
More information about the script can be found in the [Simple Config chapter](/documentation/learning_gem5/part1/simple_config) of the [Learning gem5](/documentation/learning_gem5/introduction) book.

```
build/X86/gem5.opt configs/learning_gem5/part1/simple.py
```

After running this command, you'll see gem5's output as well as `Hello world`, which comes from the hello world binary!
Now, you can start digging into how to use and extend gem5!

## Next steps

- [Learning gem5](/documentation/learning_gem5/introduction) is a work in progress book describing how to use and develop with gem5. It contains details on how to create configurations files, extend gem5 with new models, gem5's cache coherence model, and more.
- [gem5 Events](/events) are frequently occuring with computer architecture conferences and at other locations.
- You can get help on [gem5's mailing lists](/mailing_lists) or by following the [gem5 tag on Stack Overflow](https://stackoverflow.com/questions/tagged/gem5).
- [The contributing guide](/contributing) describes how to contribute your code changes and other ways to contribute to gem5.

## Tips for Using gem5 in Research

### What version of gem5 should I use?

The gem5 git repository has two branches: `develop` and `master`. The `develop`
branch contains the very latest gem5 changes **but is not stable**. It is
frequently updated. **The `develop` branch should only be used when
contributing the the gem5 project** (please see our [Contributing Guide](
/contributing) for more information on how to submit code to gem5).

The master branch contains stable gem5 code. The HEAD of the master branch
points towards the latest gem5 release. We would advise researchers use the
latest stable release of gem5 and report which version was used when publishing
results (use `git describe` to see latest gem5 release version number).

If replicating previous work, please find which version of gem5 was used. This
version should be tagged on the `master` branch and can thereby be checked-out
on a new branch using `git checkout -b {branch} {version}`.
E.g., to checkout `v19.0.0` on a new branch called `version19`:
`git checkout -b version19 v19.0.0`. A complete list of released gem5
versions can be determined by executing `git tag` on the `master` branch.

### How should I cite gem5?

You should cite the [gem5-20 paper](https://arxiv.org/abs/2007.03152).

```
The gem5 Simulator: Version 20.0+. Jason Lowe-Power, Abdul Mutaal Ahmad, Ayaz Akram, Mohammad Alian, Rico Amslinger, Matteo Andreozzi, Adrià Armejach, Nils Asmussen, Brad Beckmann, Srikant Bharadwaj, Gabe Black, Gedare Bloom, Bobby R. Bruce, Daniel Rodrigues Carvalho, Jeronimo Castrillon, Lizhong Chen, Nicolas Derumigny, Stephan Diestelhorst, Wendy Elsasser, Carlos Escuin, Marjan Fariborz, Amin Farmahini-Farahani, Pouya Fotouhi, Ryan Gambord, Jayneel Gandhi, Dibakar Gope, Thomas Grass, Anthony Gutierrez, Bagus Hanindhito, Andreas Hansson, Swapnil Haria, Austin Harris, Timothy Hayes, Adrian Herrera, Matthew Horsnell, Syed Ali Raza Jafri, Radhika Jagtap, Hanhwi Jang, Reiley Jeyapaul, Timothy M. Jones, Matthias Jung, Subash Kannoth, Hamidreza Khaleghzadeh, Yuetsu Kodama, Tushar Krishna, Tommaso Marinelli, Christian Menard, Andrea Mondelli, Miquel Moreto, Tiago Mück, Omar Naji, Krishnendra Nathella, Hoa Nguyen, Nikos Nikoleris, Lena E. Olson, Marc Orr, Binh Pham, Pablo Prieto, Trivikram Reddy, Alec Roelke, Mahyar Samani, Andreas Sandberg, Javier Setoain, Boris Shingarov, Matthew D. Sinclair, Tuan Ta, Rahul Thakur, Giacomo Travaglini, Michael Upton, Nilay Vaish, Ilias Vougioukas, William Wang, Zhengrong Wang, Norbert Wehn, Christian Weis, David A. Wood, Hongil Yoon, Éder F. Zulian. ArXiv Preprint ArXiv:2007.03152, 2021.

```

[Download the .bib file.](/assets/files/gem5-20.bib)

You may also cite the [original gem5 paper](http://dx.doi.org/10.1145/2024716.2024718).

```
The gem5 Simulator. Nathan Binkert, Bradford Beckmann, Gabriel Black, Steven K. Reinhardt, Ali Saidi, Arkaprava Basu, Joel Hestness, Derek R. Hower, Tushar Krishna, Somayeh Sardashti, Rathijit Sen, Korey Sewell, Muhammad Shoaib, Nilay Vaish, Mark D. Hill, and David A. Wood. May 2011, ACM SIGARCH Computer Architecture News.
```

You should also specify the **version** of gem5 you use in your methodology section.
If you didn't use a specific stable version of gem5 (e.g., gem5-20.1.3), you should state the commit hash *as shown on https:/gem5.googlesource.com/*.

If you use the GPU model, the DRAM model, or any of the other models in gem5 that have been [published](/publications/), you're encouraged to cite those works as well.
See [the publications page](/publications/) for a list of models that have been contributed to gem5 beyond the original paper.

### How should I refer to gem5?

"gem5" should *always* have a lowercase "g".
If it makes you uncomfortable beginning a sentence with a lowercase letter or your editor requires a capital letter, you can instead refer to gem5 as "The gem5 Simulator".

### Can I use the gem5 logo?

Absolutely!
The gem5 logo was created by [Nicole Hill](http://nicoledhill.com/) and put into the public domain under the CC0 license.
You can download the full sized logo from these links:
- [Vertical color](/assets/img/gem5logo/Color/noBackground/vertical/gem5ColorVert.png)
- [Horizontal color](/assets/img/gem5logo/Color/noBackground/horizontal/gem5ColorLong.jpg)
- [All logos (svg)](/assets/img/gem5logo/gem5masterFile.svg)

Please follow the [gem5 logo style guide](/assets/img/gem5logo/gem5styleguide.pdf) when using the gem5 logo.
More details and more versions of the logo can be found in [the source for gem5's documentation](https://github.com/gem5/new-website/tree/master/assets/img/gem5logo).
