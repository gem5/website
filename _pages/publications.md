---
layout: tabs
title: Publications
parent: about
permalink: /publications/

tabs:
  - name: Main papers
    id: main-papers
    active: true
    content: |
      If you use gem5 for your research, **please cite the following papers**.

      For your specific case, you can access a list of papers used by your project in the `citations.bib` file located in the `m5out` folder, which is generated during the build process of gem5.

      * [**The gem5 Simulator: Version 20.0+**](https://arxiv.org/abs/2007.03152). Jason Lowe-Power, Abdul Mutaal Ahmad, Ayaz Akram, Mohammad Alian, Rico Amslinger, Matteo Andreozzi, Adrià Armejach, Nils Asmussen, Brad Beckmann, Srikant Bharadwaj, Gabe Black, Gedare Bloom, Bobby R. Bruce, Daniel Rodrigues Carvalho, Jeronimo Castrillon, Lizhong Chen, Nicolas Derumigny, Stephan Diestelhorst, Wendy Elsasser, Carlos Escuin, Marjan Fariborz, Amin Farmahini-Farahani, Pouya Fotouhi, Ryan Gambord, Jayneel Gandhi, Dibakar Gope, Thomas Grass, Anthony Gutierrez, Bagus Hanindhito, Andreas Hansson, Swapnil Haria, Austin Harris, Timothy Hayes, Adrian Herrera, Matthew Horsnell, Syed Ali Raza Jafri, Radhika Jagtap, Hanhwi Jang, Reiley Jeyapaul, Timothy M. Jones, Matthias Jung, Subash Kannoth, Hamidreza Khaleghzadeh, Yuetsu Kodama, Tushar Krishna, Tommaso Marinelli, Christian Menard, Andrea Mondelli, Miquel Moreto, Tiago Mück, Omar Naji, Krishnendra Nathella, Hoa Nguyen, Nikos Nikoleris, Lena E. Olson, Marc Orr, Binh Pham, Pablo Prieto, Trivikram Reddy, Alec Roelke, Mahyar Samani, Andreas Sandberg, Javier Setoain, Boris Shingarov, Matthew D. Sinclair, Tuan Ta, Rahul Thakur, Giacomo Travaglini, Michael Upton, Nilay Vaish, Ilias Vougioukas, William Wang, Zhengrong Wang, Norbert Wehn, Christian Weis, David A. Wood, Hongil Yoon, Éder F. Zulian. CoRR, 2020. [ arXiv: [2007.03152](https://arxiv.org/abs/2007.03152) ] [ [pdf](https://arxiv.org/pdf/2007.03152.pdf) ]

      * [**The gem5 Simulator**](https://dl.acm.org/doi/10.1145/2024716.2024718). Nathan Binkert, Bradford Beckmann, Gabriel Black, Steven K. Reinhardt, Ali Saidi, Arkaprava Basu, Joel Hestness, Derek R. Hower, Tushar Krishna, Somayeh Sardashti, Rathijit Sen, Korey Sewell, Muhammad Shoaib, Nilay Vaish, Mark D. Hill, and David A. Wood. ACM SIGARCH Computer Architecture News, May 2011. [ doi: [10.1145/2024716.2024718](https://dl.acm.org/doi/10.1145/2024716.2024718) ] [ [pdf](https://dl.acm.org/doi/pdf/10.1145/2024716.2024718) ]

      * [**Simulating DRAM controllers for future system architecture exploration**](https://ieeexplore.ieee.org/document/6844484). A. Hansson, N. Agarwal, A. Kolli, T. Wenisch and A. N. Udipi. 2014 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), Monterey, CA, USA, 2014, pp. 201-210. [ doi: [10.1109/ISPASS.2014.6844484](https://doi.org/10.1109/ISPASS.2014.6844484) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6844484) ]

      * **Analyzing Local RISC-V Interrupt Latencies with Virtual Prototyping**. Robert Hauser, Lukas Steffen, Florian Grützmacher, Christian Haubelt.
      In Workshop Methoden und Beschreibungssprachen zur Modellierung und Verifikation von Schaltungen und Systemen (MBMV24), pp. 1-7, Kaiserslautern, Deutschland, Februar 2024 (to appear)


  - name: Special Features of gem5
    id: special-features
    content: |
      Additionally, we would appreciate it if you could also acknowledge the special features of gem5 that have been developed and contributed to the main line since the publication of the original paper in 2011. In simpler terms, if you use a specific feature X, please cite the corresponding paper Y from the list below.

      ### gem5art and gem5resources
      * [**Enabling Reproducible and Agile Full-System Simulation**](https://ieeexplore.ieee.org/document/9408198). Bobby R. Bruce, Hoa Nguyen, Kyle Roarty, Mahyar Samani, Marjan Friborz, Trivikram Reddy, Matthew D. Sinclair, and Jason Lowe-Power. In Proceedings of the IEEE International Symposium on Performance Analysis of Software (ISPASS), March 2021. [ doi: [10.1109/ISPASS51385.2021.00035](https://dx.doi.org/10.1109/ISPASS51385.2021.00035) ] [ [pdf](/assets/files/papers/enabling2021ispass.pdf) ]

      ### GPUs
      * [**Lost in Abstraction: Pitfalls of Analyzing GPUs at the Intermediate Language Level**](https://ieeexplore.ieee.org/document/8327041). Anthony Gutierrez, Bradford M. Beckmann, Alexandru Dutu, Joseph Gross, John Kalamatianos, Onur Kayiran, Michael LeBeane, Matthew Poremba, Brandon Potter, Sooraj Puthoor, Matthew D. Sinclair, Mark Wyse, Jieming Yin, Xianwei Zhang, Akshay Jain, Timothy G. Rogers. In Proceedings of the 24th IEEE International Symposium on High-Performance Computer Architecture (HPCA), February 2018. [ doi: [10.1109/HPCA.2018.00058](https://dx.doi.org/10.1109/HPCA.2018.00058) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8327041) ]
      * [**NoMali: Simulating a realistic graphics driver stack using a stub GPU**](http://ieeexplore.ieee.org/document/7482100). René de Jong, Andreas Sandberg. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2016. [ doi: [10.1109/ISPASS.2016.7482100](https://dx.doi.org/10.1109/ISPASS.2016.7482100) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7482100) ]
      * [**gem5-gpu: A Heterogeneous CPU-GPU Simulator**](https://ieeexplore.ieee.org/document/6709764). Jason Power, Joel Hestness, Marc S. Orr, Mark D. Hill, David A. Wood. Computer Architecture Letters vol. 13, no. 1, Jan 2014. [ doi: [10.1109/LCA.2014.2299539](https://dx.doi.org/10.1109/LCA.2014.2299539) ] [ [pdf](http://research.cs.wisc.edu/multifacet/papers/cal14_gem5gpu.pdf) ]

      ### DRAM Controller, DRAM Power Estimation
      * [**Simulating DRAM controllers for future system architecture exploration**](https://ieeexplore.ieee.org/document/6844484). Andreas Hansson, Neha Agarwal, Aasheesh Kolli, Thomas Wenisch and Aniruddha N. Udipi. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2014. [ doi: [10.1109/ISPASS.2014.6844484](https://dx.doi.org/10.1109/ISPASS.2014.6844484) ] [ [pdf](https://web.eecs.umich.edu/~twenisch/papers/ispass14.pdf) ]
      * _DRAMPower: Open-source DRAM Power & Energy Estimation Tool_. Karthik Chandrasekar, Christian Weis, Yonghui Li, Sven Goossens, Matthias Jung, Omar Naji, Benny Akesson, Norbert Wehn, and Kees Goossens, URL: [http\://www.drampower.info](http://www.drampower.info/)

      ### KVM
      * [**Full Speed Ahead: Detailed Architectural Simulation at Near-Native Speed**](http://ieeexplore.ieee.org/document/7314164). Andreas Sandberg, Nikos Nikoleris, Trevor E. Carlson, Erik Hagersten, Stefanos Kaxiras, David Black-Schaffer. IEEE International Symposium on Workload Characterization, 2015. [ doi: [10.1109/IISWC.2015.29](https://dx.doi.org/10.1109/IISWC.2015.29) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7314164) ]

      ### Elastic Traces
      * [**Exploring system performance using elastic traces: Fast, accurate and portable**](https://ieeexplore.ieee.org/document/7818336). Radhika Jagtap, Matthias Jung, Stephan Diestelhorst, Andreas Hansson, Norbert Wehn. IEEE International Conference on Embedded Computer Systems: Architectures, Modeling and Simulation (SAMOS), 2016. [ doi: [10.1109/SAMOS.2016.7818336](https://doi.org/10.1109/SAMOS.2016.7818336) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7818336) ]

      ### SystemC Coupling
      * [**System Simulation with gem5 and SystemC: The Keystone for Full Interoperability**](https://ieeexplore.ieee.org/document/8344612). C. Menard, M. Jung, J. Castrillon, N. Wehn. IEEE International Conference on Embedded Computer Systems Architectures Modeling and Simulation (SAMOS), July, 2017. [ doi: [10.1109/SAMOS.2017.8344612](https://dx.doi.org/10.1109/SAMOS.2017.8344612) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8344612) ]

  - name: Abandoned Derivative projects
    id: derivative-projects
    content: |
      Below is a list of projects that are based on gem5, are extensions of gem5, or use gem5.

      ### gem5-gpu

        - Merges 2 popular simulators: gem5 and GPGPU-Sim
        - Simulates CPUs, GPUs, and the interactions between them
        - Models a flexible memory system with support for heterogeneous
          processors and coherence
        - Supports full-system simulation through GPU driver emulation
        - [Home Page](https://gem5-gpu.cs.wisc.edu)
        - [Overview slides](http://old.gem5.org/wiki/images/7/7d/2012_12_gem5_gpu.pdf)

      ### MV5

        - MV5 is a reconfigurable simulator for heterogeneous multicore
          architectures. It is based on M5v2.0 beta 4.
        - Typical usage: simulating data-parallel applications on SIMT cores
          that operate over directory-based cache hierarchies. You can also
          add out-of-order cores to have a heterogeneous system, and all
          different types of cores can operate under the same address space
          through the same cache hierarchy.
        - Research projects based on MV5 have been published in ISCA'10,
          ICCD'09, and IPDPS'10.
        - Features
        - - Single-Instruction, Multiple-Threads (SIMT) cores
        - - Directory-based Coherence Cache: MESI/MSI. (Not based on gems/ruby)
        - - Interconnect: Fully connected and 2D Mesh. (Not based on gems/ruby)
        - - Threading API/library in system emulation mode (No support for
          full-system simulation. A benchmark suite using the thread API is
          provided)

  - name: Related to gem5
    id: related-to-gem5
    content: |
      * [**Enabling Realistic Logical Device Interface and Driver for NVM Express Enabled Full System Simulations**](https://link.springer.com/article/10.1007%2Fs10766-017-0530-1). Donghyun Gouk, Jie Zhang and Myoungsoo Jung. IFIP International Conference on Network and Parallel Computing (NPC) and Invited for International Journal of Parallel Programming (IJPP), 2017. [ doi: [10.1007/s10766-017-0530-1](https://dx.doi.org/10.1007/s10766-017-0530-1) ] [ [pdf](https://link.springer.com/content/pdf/10.1007/s10766-017-0530-1.pdf) ]

      * [**SimpleSSD: Modeling Solid State Drives for Holistic System Simulation**](https://ieeexplore.ieee.org/document/8031080). Myoungsoo Jung, Jie Zhang, Ahmed Abulila, Miryeong Kwon, Narges Shahidi, John Shalf, Nam Sung Kim and Mahmut Kandemir. IEEE Computer Architecture Letters (CAL), 2017. [ doi: [10.1109/LCA.2017.2750658](https://dx.doi.org/10.1109/LCA.2017.2750658) ] [ arXiv: [1705.06419](https://arxiv.org/abs/1705.06419) \[cs.AR\] ]

      * [**dist-gem5: Distributed Simulation of Computer Clusters**](https://ieeexplore.ieee.org/document/7975287). Mohammad Alian, Gabor Dozsa, Umur Darbaz, Stephan Diestelhorst, Daehoon Kim, and Nam Sung Kim. IEEE International Symposium on Performance Analysis of Systems (ISPASS), April 2017. [ doi: [10.1109/ISPASS.2017.7975287](https://dx.doi.org/10.1109/ISPASS.2017.7975287) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7975287) ]

      * [**pd-gem5: Simulation Infrastructure for Parallel/Distributed Computer Systems**](https://ieeexplore.ieee.org/document/7114236). Mohammad Alian, Daehoon Kim, and Nam Sung Kim. Computer Architecture Letters (CAL), 2016. [ doi: [10.1109/LCA.2015.2438295](https://dx.doi.org/10.1109/LCA.2015.2438295) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7114236) ]

      * [**A Full-System Approach to Analyze the Impact of Next-Generation Mobile Flash Storage**](https://ieeexplore.ieee.org/document/7095809). Rene de Jong and Andreas Hansson. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2015. [ doi: [10.1109/ISPASS.2015.7095809](https://dx.doi.org/10.1109/ISPASS.2015.7095809) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7095809) ]

      * [**Sources of Error in Full-System Simulation**](https://ieeexplore.ieee.org/document/6844457). A. Gutierrez, J. Pusdesris, R.G. Dreslinski, T. Mudge, C. Sudanthi, C.D. Emmons, M. Hayenga, and N. Paver. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2014. [ doi: [10.1109/ISPASS.2014.6844457](https://doi.org/10.1109/ISPASS.2014.6844457) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6844457) ]

      * [**Introducing DVFS-Management in a Full-System Simulator**](https://ieeexplore.ieee.org/document/6730810). Vasileios Spiliopoulos, Akash Bagdia, Andreas Hansson, Peter Aldworth and Stefanos Kaxiras. In Proceedings of the 21st International Symposium on Modeling, Analysis & Simulation of Computer and Telecommunication Systems (MASCOTS), August 2013. [ doi: [10.1109/MASCOTS.2013.75](https://doi.org/10.1109/MASCOTS.2013.75) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6730810) ]

      * [**Accuracy Evaluation of GEM5 Simulator System**](https://ieeexplore.ieee.org/document/6322869). A. Butko, R. Garibotti, L. Ost, and G. Sassatelli. In the proceeding of the IEEE International Workshop on Reconfigurable Communication-centric Systems-on-Chip (ReCoSoC), York, United Kingdom, July 2012. [ doi: [10.1109/ReCoSoC.2012.6322869](http://dx.doi.org/10.1109/ReCoSoC.2012.6322869) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6322869) ]

      * [**The M5 Simulator: Modeling Networked Systems**](https://ieeexplore.ieee.org/document/1677503). N. L. Binkert, R. G. Dreslinski, L. R. Hsu, K. T. Lim, A. G. Saidi, S. K. Reinhardt. IEEE Micro, vol. 26, no. 4, pp. 52-60, July/August, 2006. [ doi: [10.1109/MM.2006.82](http://dx.doi.org/10.1109/MM.2006.82) ] [ [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1677503) ]

      * [**Multifacet’s General Execution-driven Multiprocessor Simulator (GEMS) Toolset**](https://dl.acm.org/doi/10.1145/1105734.1105747). Milo M.K. Martin, Daniel J. Sorin, Bradford M. Beckmann, Michael R. Marty, Min Xu, Alaa R. Alameldeen, Kevin E. Moore, Mark D. Hill, and David A. Wood. Computer Architecture News (CAN), September 2005. [ doi: [10.1145/1105734.1105747](http://dx.doi.org/10.1145/1105734.1105747) ] [ [pdf](https://dl.acm.org/doi/pdf/10.1145/1105734.1105747) ]

  - name: Using gem5
    id: using-gem5
    content: |
      Please visit [Google Scholar](https://scholar.google.com/scholar?q=gem5) page for a list of all papers that use gem5.
---