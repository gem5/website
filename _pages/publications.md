---
layout: toc
title: Publications
parent: about
permalink: /publications/
---
* TOC
{:toc}

If you use gem5 in your research, we would appreciate a citation to the original paper in any publications you produce. Moreover, we would appreciate if you cite also the speacial features of gem5 which have been developed and contributed to the main line since the publication of the original paper in 2011\. In other words, if you use feature X please also cite the according paper Y from the list below.


# Original Paper<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#original-paper"></span>
---
*   [**The gem5 Simulator**](http://dx.doi.org/10.1145/2024716.2024718). Nathan Binkert, Bradford Beckmann, Gabriel Black, Steven K. Reinhardt, Ali Saidi, Arkaprava Basu, Joel Hestness, Derek R. Hower, Tushar Krishna, Somayeh Sardashti, Rathijit Sen, Korey Sewell, Muhammad Shoaib, Nilay Vaish, Mark D. Hill, and David A. Wood. May 2011, ACM SIGARCH Computer Architecture News.



# Special Features of gem5<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#special-features-of-gem5"></span>
---

## gem5art and gem5resources<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#gem5art"></span>

* [**Enabling Reproducible and Agile Full-System Simulation**](/assets/files/papers/enabling2021ispass.pdf). Bobby R. Bruce, Hoa Nguyen, Kyle Roarty, Mahyar Samani, Marjan Friborz, Trivikram Reddy, Matthew D. Sinclair, and Jason Lowe-Power. In Proceedings of the IEEE International Symposium on Performance Analysis of Software (ISPASS), March 2021.


## GPUs<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#gpus"></span>

*   [**Lost in Abstraction: Pitfalls of Analyzing GPUs at the Intermediate Language Level**](https://doi.org/10.1109/HPCA.2018.00058). Anthony Gutierrez, Bradford M. Beckmann, Alexandru Dutu, Joseph Gross, John Kalamatianos, Onur Kayiran, Michael LeBeane, Matthew Poremba, Brandon Potter, Sooraj Puthoor, Matthew D. Sinclair, Mark Wyse, Jieming Yin, Xianwei Zhang, Akshay Jain, Timothy G. Rogers. In Proceedings of the 24th IEEE International Symposium on High-Performance Computer Architecture (HPCA), February 2018.

*   [**NoMali: Simulating a realistic graphics driver stack using a stub GPU**](http://ieeexplore.ieee.org/document/7482100/). René de Jong, Andreas Sandberg. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2016.

*   [**gem5-gpu: A Heterogeneous CPU-GPU Simulator**](http://research.cs.wisc.edu/multifacet/papers/cal14_gem5gpu.pdf). Jason Power, Joel Hestness, Marc S. Orr, Mark D. Hill, David A. Wood. Computer Architecture Letters vol. 13, no. 1, Jan 2014

## DRAM Controller, DRAM Power Estimation<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#dram-controller-dram-power-estimation"></span>

*   [**Simulating DRAM controllers for future system architecture exploration**](http://www.ics.ele.tue.nl/~mhansson/documents/pdf/2014-ispass.pdf). Andreas Hansson, Neha Agarwal, Aasheesh Kolli, Thomas Wenisch and Aniruddha N. Udipi. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2014.

*   [**DRAMPower: Open-source DRAM Power & Energy Estimation Tool**](http://www.drampower.info). Karthik Chandrasekar, Christian Weis, Yonghui Li, Sven Goossens, Matthias Jung, Omar Naji, Benny Akesson, Norbert Wehn, and Kees Goossens, URL: [http://www.drampower.info](http://www.drampower.info).

## KVM<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#kvm"></span>

*   [**Full Speed Ahead: Detailed Architectural Simulation at Near-Native Speed**](http://ieeexplore.ieee.org/document/7314164/). Andreas Sandberg, Nikos Nikoleris, Trevor E. Carlson, Erik Hagersten, Stefanos Kaxiras, David Black-Schaffer. 2015 IEEE International Symposium on Workload Characterization

## Elastic Traces<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#elastic-traces"></span>

*   [**Exploring system performance using elastic traces: Fast, accurate and portable**](https://doi.org/10.1109/SAMOS.2016.7818336). Radhika Jagtap, Matthias Jung, Stephan Diestelhorst, Andreas Hansson, Norbert Wehn. IEEE International Conference on Embedded Computer Systems: Architectures, Modeling and Simulation (SAMOS), 2016

## SystemC Coupling<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#systemc-coupling"></span>

*   [**System Simulation with gem5 and SystemC: The Keystone for Full Interoperability**](https://ieeexplore.ieee.org/document/8344612). C. Menard, M. Jung, J. Castrillon, N. Wehn. IEEE International Conference on Embedded Computer Systems Architectures Modeling and Simulation (SAMOS), July, 2017

# Derivative projects

Below is a list of projects that are based on gem5, are extensions of
gem5, or use gem5.

## gem5-gpu

  - Merges 2 popular simulators: gem5 and GPGPU-Sim
  - Simulates CPUs, GPUs, and the interactions between them
  - Models a flexible memory system with support for heterogeneous
    processors and coherence
  - Supports full-system simulation through GPU driver emulation

### Resources

  - [Home Page](https://gem5-gpu.cs.wisc.edu)
  - [Overview slides](http://gem5.org/wiki/images/7/7d/2012_12_gem5_gpu.pdf)
  - [Mailing list](http://groups.google.com/group/gem5-gpu-dev)

## MV5

  - MV5 is a reconfigurable simulator for heterogeneous multicore
    architectures. It is based on M5v2.0 beta 4.
  - Typical usage: simulating data-parallel applications on SIMT cores
    that operate over directory-based cache hierarchies. You can also
    add out-of-order cores to have a heterogeneous system, and all
    different types of cores can operate under the same address space
    through the same cache hierarchy.
  - Research projects based on MV5 have been published in ISCA'10,
    ICCD'09, and IPDPS'10.

### Features

  - Single-Instruction, Multiple-Threads (SIMT) cores
  - Directory-based Coherence Cache: MESI/MSI. (Not based on gems/ruby)
  - Interconnect: Fully connected and 2D Mesh. (Not based on gems/ruby)
  - Threading API/library in system emulation mode (No support for
    full-system simulation. A benchmark suite using the thread API is
    provided)

### Resources

  - [Home Page](https://sites.google.com/site/mv5sim/home)
  - [Tutorial at ISPASS '11](https://sites.google.com/site/mv5sim/tutorial)
  - [Google group](http://groups.google.com/group/mv5sim)

# Other Publications related to gem5<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#other-publications-related-to-gem5"></span>
---
*   [**Enabling Realistic Logical Device Interface and Driver for NVM Express Enabled Full System Simulations**](http://simplessd.camelab.org). Donghyun Gouk, Jie Zhang and Myoungsoo Jung. IFIP International Conference on Network and Parallel Computing (NPC) and Invited for International Journal of Parallel Programming (IJPP), 2017

*   [**SimpleSSD: Modeling Solid State Drives for Holistic System Simulation**](https://arxiv.org/pdf/1705.06419.pdf). Myoungsoo Jung, Jie Zhang, Ahmed Abulila, Miryeong Kwon, Narges Shahidi, John Shalf, Nam Sung Kim and Mahmut Kandemir. IEEE Computer Architecture Letters (CAL), 2017

*   “dist-gem5: Distributed Simulation of Computer Clusters,” Mohammad Alian, Gabor Dozsa, Umur Darbaz, Stephan Diestelhorst, Daehoon Kim, and Nam Sung Kim. IEEE International Symposium on Performance Analysis of Systems (ISPASS), April 2017

*   [**pd-gem5: Simulation Infrastructure for Parallel/Distributed Computer Systems**](https://publish.illinois.edu/icsl-pdgem5/publications). Mohammad Alian, Daehoon Kim, and Nam Sung Kim. Computer Architecture Letters (CAL), 2016.

*   [**A Full-System Approach to Analyze the Impact of Next-Generation Mobile Flash Storage**](http://www.ics.ele.tue.nl/~mhansson/documents/pdf/2015-ispass.pdf). Rene de Jong and Andreas Hansson. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2015.

*   [**Sources of Error in Full-System Simulation**](https://doi.org/10.1109/ISPASS.2014.6844457). A. Gutierrez, J. Pusdesris, R.G. Dreslinski, T. Mudge, C. Sudanthi, C.D. Emmons, M. Hayenga, and N. Paver. In Proceedings of the International Symposium on Performance Analysis of Systems and Software (ISPASS), March 2014.

*   [**Introducing DVFS-Management in a Full-System Simulator**](http://www.ics.ele.tue.nl/~mhansson/documents/pdf/2013-mascots.pdf). Vasileios Spiliopoulos, Akash Bagdia, Andreas Hansson, Peter Aldworth and Stefanos Kaxiras. In Proceedings of the 21st International Symposium on Modeling, Analysis & Simulation of Computer and Telecommunication Systems (MASCOTS), August 2013.

*   [**Accuracy Evaluation of GEM5 Simulator System**](http://dx.doi.org/10.1109/ReCoSoC.2012.6322869). A. Butko, R. Garibotti, L. Ost, and G. Sassatelli. In the proceeding of the IEEE International Workshop on Reconfigurable Communication-centric Systems-on-Chip (ReCoSoC), York, United Kingdom, July 2012.
*   [**The M5 Simulator: Modeling Networked Systems**](http://dx.doi.org/10.1109/MM.2006.82). N. L. Binkert, R. G. Dreslinski, L. R. Hsu, K. T. Lim, A. G. Saidi, S. K. Reinhardt. IEEE Micro, vol. 26, no. 4, pp. 52-60, July/August, 2006.
*   [**Multifacet’s General Execution-driven Multiprocessor Simulator (GEMS) Toolset**](http://dx.doi.org/10.1145/1105734.1105747). Milo M.K. Martin, Daniel J. Sorin, Bradford M. Beckmann, Michael R. Marty, Min Xu, Alaa R. Alameldeen, Kevin E. Moore, Mark D. Hill, and David A. Wood. Computer Architecture News (CAN), September 2005.

# Publications using gem5 / m5<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#publications-using-gem5-m5"></span>
---
## 2017<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2017"></span>

*   [[https://chess.eecs.berkeley.edu/pubs/1194/KimEtAl_CyPhy17.pdf](https://chess.eecs.berkeley.edu/pubs/1194/KimEtAl_CyPhy17.pdf)**An Integrated Simulation Tool for Computer Architecture and Cyber-Physical Systems**]. Hokeun Kim, Armin Wasicek, and Edward A. Lee. In Proceedings of the 6th Workshop on Design, Modeling and Evaluation of Cyber-Physical Systems (CyPhy’17), Seoul, Korea, October 19, 2017.

*   [[http://www.lirmm.fr/~sassate/ADAC/wp-content/uploads/2017/06/opensuco17.pdf](http://www.lirmm.fr/~sassate/ADAC/wp-content/uploads/2017/06/opensuco17.pdf)**Efficient Programming for Multicore Processor Heterogeneity: OpenMP versus OmpSs**]. Anastasiia Butko, Florent Bruguier, Abdoulaye Gamatié and Gilles Sassatelli. In Open Source Supercomputing (OpenSuCo’17) Workshop co-located with ISC’17, June 2017.

*   [[https://hal-lirmm.ccsd.cnrs.fr/lirmm-01467328](https://hal-lirmm.ccsd.cnrs.fr/lirmm-01467328)**MAGPIE: System-level Evaluation of Manycore Systems with Emerging Memory Technologies**]. Thibaud Delobelle, Pierre-Yves Péneau, Abdoulaye Gamatié, Florent Bruguier, Sophiane Senni, Gilles Sassatelli and Lionel Torres, 2nd International Workshop on Emerging Memory Solutions (EMS) co-located with DATE’17, March 2017.

## 2016<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2016"></span>

*   [[http://ieeexplore.ieee.org/document/7776838](http://ieeexplore.ieee.org/document/7776838)**An Agile Post-Silicon Validation Methodology for the Address Translation Mechanisms of Modern Microprocessors**]. G. Papadimitriou, A. Chatzidimitriou, D. Gizopoulos, R. Morad, IEEE Transactions on Device and Materials Reliability (TDMR 2016), Volume: PP, Issue: 99, December 2016.

*   [[http://ieeexplore.ieee.org/document/7753339](http://ieeexplore.ieee.org/document/7753339)**Unveiling Difficult Bugs in Address Translation Caching Arrays for Effective Post-Silicon Validation**]. G. Papadimitriou, D. Gizopoulos, A. Chatzidimitriou, T. Kolan, A. Koyfman, R. Morad, V. Sokhin, IEEE International Conference on Computer Design (ICCD 2016), Phoenix, AZ, USA, October 2016.

*   [[http://ieeexplore.ieee.org/document/7833682/](http://ieeexplore.ieee.org/document/7833682/)**Loop optimization in presence of STT-MRAM caches: A study of performance-energy tradeoffs**]. Pierre-Yves Péneau, Rabab Bouziane, Abdoulaye Gamatié, Erven Rohou, Florent Bruguier, Gilles Sassatelli, Lionel Torres and Sophiane Senni, 26th International Workshop on Power and Timing Modeling, Optimization and Simulation (PATMOS), September 21-23 2016.

*   [[http://ieeexplore.ieee.org/abstract/document/7774439](http://ieeexplore.ieee.org/abstract/document/7774439)**Full-System Simulation of big.LITTLE Multicore Architecture for Performance and Energy Exploration**]. Anastasiia Butko, Florent Bruguier, Abdoulaye Gamatié, Gilles Sassatelli, David Novo, Lionel Torres and Michel Robert. Embedded Multicore/Many-core Systems-on-Chip (MCSoC), 2016 IEEE 10th International Symposium on, September 21-23, 2016.

*   [[http://ieeexplore.ieee.org/document/7448986](http://ieeexplore.ieee.org/document/7448986)**Exploring MRAM Technologies for Energy Efficient Systems-On-Chip**]. Sophiane Senni, Lionel Torres, Gilles Sassatelli, Abdoulaye Gamatié and Bruno Mussard, IEEE Journal on Emerging and Selected Topics in Circuits and Systems , Volume: 6, Issue: 3, Sept. 2016.

*   [[https://cpc2016.infor.uva.es/wp-content/uploads/2016/06/CPC2016_paper_11.pdf](https://cpc2016.infor.uva.es/wp-content/uploads/2016/06/CPC2016_paper_11.pdf)**Architectural exploration of heterogeneous memory systems**]. Marcos Horro, Gabriel Rodríguez, Juan Touriño and Mahmut T. Kandemir. 19th Workshop on Compilers for Parallel Computing (CPC), July 2016.

*   [[http://ieeexplore.ieee.org/document/7604675](http://ieeexplore.ieee.org/document/7604675)**ISA-Independent Post-Silicon Validation for the Address Translation Mechanisms of Modern Microprocessors**]. G. Papadimitriou, A. Chatzidimitriou, D. Gizopoulos and R. Morad, IEEE International Symposium on On-Line Testing and Robust System Design (IOLTS 2016), Sant Feliu de Guixols, Spain, July 2016.

*   [**Anatomy of microarchitecture-level reliability assessment: Throughput and accuracy**](http://ieeexplore.ieee.org/document/7482075). A.Chatzidimitriou, D.Gizopoulos, IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), Uppsala, Sweden, April 2016.

*   [**Agave: A benchmark suite for exploring the complexities of the Android software stack**](http://ieeexplore.ieee.org/document/7482089). Martin Brown, Zachary Yannes, Michael Lustig, Mazdak Sanati, Sally A. McKee, Gary S. Tyson, Steven K. Reinhardt, IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), Uppsala, Sweden, April 2016.

## 2015<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2015"></span>

*   [[http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=7314163](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=7314163)**Differential Fault Injection on Microarchitectural Simulators**]. M.Kaliorakis, S.Tselonis, A.Chatzidimitriou, N.Foutris, D.Gizopoulos, IEEE International Symposium on Workload Characterization (IISWC), Atlanta, GA, USA, October 2015.

*   [**Live Introspection of Target-Agnostic JIT in Simulation**](http://www.esug.org/wiki/pier/Conferences/2015/International-Workshop-IWST_15). B. Shingarov. International Workshop IWST’15 in cooperation with ACM, Brescia, Italy, 2015.

*   [**Security in MPSoCs: A NoC Firewall and an Evaluation Framework**](http://dx.doi.org/10.1109/TCAD.2015.2448684). M.D. Grammatikakis, K. Papadimitriou, P. Petrakis, A. Papagrigoriou, G. Kornaros, I. Christoforakis, O. Tomoutzoglou, G. Tsamis and M. Coppola. In IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), vol.34, no.8, pp.1344-1357, Aug. 2015

*   [**DPCS: Dynamic Power/Capacity Scaling for SRAM Caches in the Nanoscale Era.**](http://dx.doi.org/10.1145/2792982) Mark Gottscho, Abbas BanaiyanMofrad, Nikil Dutt, Alex Nicolau, and Puneet Gupta. ACM Transactions on Architecture and Code Optimization (TACO), Vol. 12, No. 3, Article 27\. Pre-print June 2015, published August 2015, print October 2015.

*   [**A predictable and command-level priority-based DRAM controller for mixed-criticality systems**](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=7108455). Hokeun Kim, David Broman, Edward A. Lee, Michael Zimmer, Aviral Shrivastava, Junkwang Oh. Proceedings of the 21st IEEE Real-Time and Embedded Technology and Application Symposium (RTAS), Seattle, WA, USA, April, 2015.

*   [**Security Enhancements for Building Saturation-free, Low-Power NoC-based MPSoCs**](http://spicy2015.di.unimi.it/index.php?pageid=program). Kyprianos Papadimitriou, Polydoros Petrakis, Miltos Grammatikakis, Marcello Coppola. In IEEE Conference on Communications and Network Security (CNS) - 1st IEEE Workshop on Security and Privacy in Cybermatics, Florence, Italy, 2015

*   [**Design Exploration For Next Generation High-Performance Manycore On-chip Systems: Application To big.LITTLE Architectures**](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=7309629). Anastasiia Butko, Abdoulaye Gamatie, Gilles Sassatelli, Lionel Torres and Michel Robert. VLSI (ISVLSI), 2015 IEEE Computer Society Annual Symposium on, July 10, 2015

*   [[http://dx.doi.org/10.1007/s11227-014-1375-7](http://dx.doi.org/10.1007/s11227-014-1375-7) **Gem5v: a modified gem5 for simulating virtualized systems]**. Seyed Hossein Nikounia, Siamak Mohammadi. Springer Journal of Supercomputing. The source code is available [[https://github.com/nikoonia/gem5v](https://github.com/nikoonia/gem5v) **here]**.

*   [**Micro-architectural simulation of embedded core heterogeneity with gem5 and McPAT**](http://dx.doi.org/10.1145/2693433.2693440). Fernando A. Endo, Damien Couroussé, Henri-Pierre Charles. RAPIDO ‘15 Proceedings of the 2015 Workshop on Rapid Simulation and Performance Evaluation: Methods and Tools. January 2015.

*   [**A trace-driven approach for fast and accurate simulation of manycore architectures**](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=7059093&queryText%3DA+trace-driven+approach+for+fast+and+accurate+simulation+of+manycore+architectures). Anastasiia Butko, Rafael Garibotti, Luciano Ost, Vianney Lapotre, Abdoulaye Gamatie, Gilles Sassatelli and Chris Adeniyi-Jones. Design Automation Conference (ASP-DAC), 2015 20th Asia and South Pacific. January 19, 2015

## 2014<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2014"></span>

*   [**Evaluating Private vs. Shared Last-Level Caches for Energy Efficiency in Asymmetric Multi-Cores**](https://doi.org/10.1109/SAMOS.2014.6893211). A. Gutierrez, R.G. Dreslinski, and Trevor Mudge. In Proceedings of the 14th International Conference on Embedded Computer Systems: Architectures, Modeling, and Simulation (SAMOS), 2014.

*   [[http://dx.doi.org/10.1109/HPCC.2014.173](http://dx.doi.org/10.1109/HPCC.2014.173) **Security Effectiveness and a Hardware Firewall for MPSoCs]**. M. D. Grammatikakis, K. Papadimitriou, P. Petrakis, A. Papagrigoriou, G. Kornaros, I. Christoforakis and M. Coppola. In 16th IEEE International Conference on High Performance Computing and Communications - Workshop on Multicore and Multithreaded Architectures and Algorithms, 2014, pp. 1032-1039 Aug. 2014

*   [[http://dx.doi.org/10.1145/2541940.2541951](http://dx.doi.org/10.1145/2541940.2541951) **Integrated 3D-Stacked Server Designs for Increasing Physical Density of Key-Value Stores]**. Anthony Gutierrez, Michael Cieslak, Bharan Giridhar, Ronald G. Dreslinski, Luis Ceze, and Trevor Mudge. ASPLOS XIX

*   [[http://dx.doi.org/10.1145/2593069.2593184](http://dx.doi.org/10.1145/2593069.2593184) **Power / Capacity Scaling: Energy Savings With Simple Fault-Tolerant Caches]**. Mark Gottscho, Abbas BanaiyanMofrad, Nikil Dutt, Alex Nicolau, and Puneet Gupta. DAC, 2014.

*   [”‘Write-Aware Replacement Policies for PCM-Based Systems “’](http://dx.doi.org/10.1093/comjnl/bxu104). R. Rodríguez-Rodríguez, F. Castro, D. Chaver*, R. Gonzalez-Alberquilla, L. Piñuel and F. Tirado. The Computer Journal, 2014.

*   [”‘Micro-architectural simulation of in-order and out-of-order ARM microprocessors with gem5 “’](http://dx.doi.org/10.1109/SAMOS.2014.6893220). Fernando A. Endo, Damien Couroussé, Henri-Pierre Charles. 2014 International Conference on Embedded Computer Systems: Architectures, Modeling, and Simulation (SAMOS XIV). July 2014.

## 2013<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2013"></span>

*   [**Continuous Real-World Inputs Can Open Up Alternative Accelerator Designs**](http://doi.acm.org/10.1145/2485922.2485923). Bilel Belhadj, Antoine Joubert, Zheng Li, Rodolphe Héliot, and Olivier Temam. ISCA ‘13
*   _Cache Coherence for GPU Architectures._ Inderpreet Singh, Arrvindh Shriraman, Wilson WL Fung, Mike O’Connor, and Tor M. Aamodt. HPCA, 2013.
*   _Navigating Heterogeneous Processors with Market Mechanisms._ Marisabel Guevara, Benjamin Lubin, and Benjamin C. Lee. HPCA, 2013
*   _Power Struggles: Revisiting the RISC vs. CISC Debate on Contemporary ARM and x86 Architectures_. Emily Blem, Jaikrishnan Menon, and Karthikeyan Sankaralingam. HPCA 2013.
*   [**Coset coding to extend the lifetime of memory**](http://dx.doi.org/10.1109/HPCA.2013.6522321). Adam N. Jacobvitz, Robert Calderbank, Daniel J. Sorin. HPCA ‘13.
*   [**The McPAT Framework for Multicore and Manycore Architectures: Simultaneously Modeling Power, Area, and Timing**](http://dx.doi.org/10.1145/2445572.2445577). Sheng Li, Jung Ho Ahn, Richard D. Strong, Jay B. Brockman, Dean M. Tullsen, Norman P. Jouppi. ACM Transactions on Architecture and Code Optimization (TACO), Volume 10, Issue 1, April 2013
*   [**Optimization and Mathematical Modeling in Computer Architecture**](http://dx.doi.org/10.2200/S00531ED1V01Y201308CAC026) Nowatzki, T., Ferris, M., Sankaralingam, K., Estan, C., Vaish, N., & Wood, David A. (2013). Synthesis Lectures on Computer Architecture, 8(4), 1-144.
*   [**Limits of Parallelism and Boosting in Dim Silicon**](http://doi.ieeecomputersociety.org/10.1109/MM.2013.73). Nathaniel Pinckney, Ronald G. Dreslinski, Korey Sewell, David Fick, Trevor Mudge, Dennis Sylvester, David Blaauw, IEEE Micro, vol. 33, no. 5, pp. 30-37, Sept.-Oct., 2013

## 2012<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2012"></span>

*   _Hardware Prefetchers for Emerging Parallel Applications_, Biswabandan Panda, Shankar Balachandran. In the proceedings of the IEEE/ACM Parallel Architectures and Compilation Techniques,PACT, Minneapolis, October 2012.
*   [**Lazy Cache Invalidation for Self-Modifying Codes**](https://doi.org/10.1145/2380403.2380433). A. Gutierrez, J. Pusdesris, R.G. Dreslinski, and T. Mudge. In the proceedings of the International Conference on Compilers, Architecture and Synthesis for Embedded Systems (CASES), Tampere, Finland, October 2012.
*   _Accuracy Evaluation of GEM5 Simulator System_. A. Butko, R. Garibotti, L. Ost, and G. Sassatelli. In the proceeding of the IEEE International Workshop on Reconfigurable Communication-centric Systems-on-Chip (ReCoSoC), York, United Kingdom, July 2012.
*   _Viper: Virtual Pipelines for Enhanced Reliability_. A. Pellegrini, J. L. Greathouse, and V. Bertacco. In the proceedings of the International Symposium on Computer Architecture (ISCA), Portland, OR, June 2012.
*   [**Reducing memory reference energy with opportunistic virtual caching**](http://dx.doi.org/10.1109/ISCA.2012.6237026). Arkaprava Basu, Mark D. Hill, Michael M. Swift. In the proceedings of the 39th International Symposium on Computer Architecture (ISCA 2012).
*   [**Cache Revive: Architecting Volatile STT-RAM Caches for Enhanced Performance in CMPs**](http://www.cse.psu.edu/~axj936/docs/Revive-DAC-2012.pdf). Adwait Jog, Asit Mishra, Cong Xu, Yuan Xie, V. Narayanan, Ravi Iyer, Chita Das. In the proceedings oF the IEEE/ACM Design Automation Conference (DAC), San Francisco, CA, June 2012.

## 2011<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2011"></span>

*   [**Full-System Analysis and Characterization of Interactive Smartphone Applications**](https://doi.org/10.1109/IISWC.2011.6114205). A. Gutierrez, R.G. Dreslinski, T.F. Wenisch, T. Mudge, A. Saidi, C. Emmons, and N. Paver. In the proceeding of the IEEE International Symposium on Workload Characterization (IISWC), pages 81-90, Austin, TX, November 2011.
*   _Universal Rules Guided Design Parameter Selection for Soft Error Resilient Processors,_ L. Duan, Y. Zhang, B. Li, and L. Peng. Proceedings of the International Symposium on Performance Analysis of Systems and Software(ISPASS), Austin, TX, April 2011.

## 2010<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2010"></span>

*   _Using Hardware Vulnerability Factors to Enhance AVF Analysis,_ V. Sridharan, D. R. Kaeli. Proceedings of the International Symposium on Computer Architecture (ISCA-37), Saint-Malo, France, June 2010.
*   _Leveraging Unused Cache Block Words to Reduce Power in CMP Interconnect,_ H. Kim, P. Gratz. IEEE Computer Architecture Letters, vol. 99, (RapidPosts), 2010.
*   _A Fast Timing-Accurate MPSoC HW/SW Co-Simulation Platform based on a Novel Synchronization Scheme,_ Mingyan Yu, Junjie Song, Fangfa Fu, Siyue Sun, and Bo Liu. Proceedings of the International MultiConfernce of Engineers and Computer Scientists. 2010 [pdf](http://www.iaeng.org/publication/IMECS2010/IMECS2010_pp1396-1400.pdf)
*   _Simulation of Standard Benchmarks in Hardware Implementations of L2 Cache Models in Verilog HDL,_ Rosario M. Reas, Anastacia B. Alvarez, Joy Alinda P. Reyes, Computer Modeling and Simulation, International Conference on, pp. 153-158, 2010 12th International Conference on Computer Modelling and Simulation, 2010
*   _A Simulation of Cache Sub-banking and Block Buffering as Power Reduction Techniques for Multiprocessor Cache Design,_ Jestoni V. Zarsuela, Anastacia Alvarez, Joy Alinda Reyes, Computer Modeling and Simulation, International Conference on, pp. 515-520, 2010 12th International Conference on Computer Modelling and Simulation, 2010

## 2009<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2009"></span>

*   _Efﬁcient Implementation of Decoupling Capacitors in 3D Processor-DRAM Integrated Computing Systems._ Q. Wu, J. Lu, K. Rose, and T. Zhang. Great Lakes Symposium on VLSI. 2009.
*   _Evaluating the Impact of Job Scheduling and Power Management on Processor Lifetime for Chip Multiprocessors._ A. K. Coskun, R. Strong, D. M. Tullsen, and T. S. Rosing. Proceedings of the eleventh international joint conference on Measurement and modeling of computer systems. 2009.
*   ” Devices and architectures for photonic chip-scale integration.” J. Ahn, M. Fiorentino1, R. G. Beausoleil, N. Binkert, A. Davis, D. Fattal, N. P. Jouppi, M. McLaren, C. M. Santori, R. S. Schreiber, S. M. Spillane, D. Vantrease and Q. Xu. Journal of Applied Physics A: Materials Science & Processing. February 2009.
*   _System-Level Power, Thermal and Reliability Optimization._ C. Zhu. Thesis at Queen’s University. 2009.

*   _A light-weight fairness mechanism for chip multiprocessor memory systems._ M. Jahre, L. Natvig. Proceedings of the 6th ACM conference on Computing Frontiers. 2009.
*   _Decoupled DIMM: building high-bandwidth memory system using low-speed DRAM devices._ H. Zheng, J. Lin, Z. Zhang, and Z. Zhu. International Symposium on Computer Architecture (ISCA). 2009.
*   _On the Performance of Commit-Time-Locking Based Software Transactional Memory._ Z. He and B. Hong. The 11th IEEE International Conference on. High Performance Computing and Communications (HPCC-09). 2009.

*   _A Quantitative Study of Memory System Interference in Chip Multiprocessor Architectures._ M. Jahre, M. Grannaes and L. Natvig. The 11th IEEE International Conference on. High Performance Computing and Communications (HPCC-09). 2009.
*   _Hardware Support for Debugging Message Passing Applications for Many-Core Architectures._ C. Svensson. Masters Thesis at the University of Illinois at Urbana-Champaign, 2009.
*   _Initial Experiments in Visualizing Fine-Grained Execution of Parallel Software Through Cycle-Level Simulation._ R. Strong, J. Mudigonda, J. C. Mogul, N. Binkert. USENIX Workshop on Hot Topics in Parallelism (HotPar). 2009.
*   _MPreplay: Architecture Support for Deterministic Replay of Message Passing Programs on Message Passing Many-core Processors._ C. Erik-Svensson, D. Kesler, R. Kumar, and G. Pokam. University of Illinois Technical Report number UILU-09-2209.
*   _Low-power Inter-core Communication through Cache Partitioning in Embedded Multiprocessors._ C. Yu, X. Zhou, and P. Petrov .Symposium on Integrated Circuits and System Design (sbcci). 2009.
*   _Integrating NAND flash devices onto servers._ D. Roberts, T. Kgil, T. Mudge. Communications of the ACM (CACM). 2009.
*   _A High-Performance Low-Power Nanophotonic On-Chip Network._ Z. Li, J. Wu, L. Shang, A. Mickelson, M. Vachharajani, D. Filipovic, W. Park∗ and Y. Sun. International Symposium on Low Power Electronic Design (ISLPED). 2009.
*   _Core monitors: monitoring performance in multicore processors._ P. West, Y. Peress, G. S. Tyson, and S. A. McKee. Computing Frontiers. 2009.
*   _Parallel Assertion Processing using Memory Snapshots._ M. F. Iqbal, J. H. Siddiqui, and D. Chiou. Workshop on Unique Chips and Systems (UCAS). April 2009.
*   _Leveraging Memory Level Parallelism Using Dynamic Warp Subdivision._ J. Meng, D. Tarjan, and K. Skadron. Univ. of Virginia Dept. of Comp. Sci. Tech Report (CS-2009-02).
*   _Reconfigurable Multicore Server Processors for Low Power Operation._ R. G. Dreslinski, D. Fick, D. Blaauw, D. Sylvester and T. Mudge. 9th International Symposium on Systems, Architectures, MOdeling and Simulation (SAMOS). July 2009.
*   _Near Threshold Computing: Overcoming Performance Degradation from Aggressive Voltage Scaling_ R. G. Dreslinski, M. Wieckowski, D. Blaauw, D. Sylvester, and T. Mudge. Workshop on Energy Efficient Design (WEED), June 2009.
*   _Workload Adaptive Shared Memory Multicore Processors with Reconfigurable Interconnects._ S. Akram, R. Kumar, and D. Chen. IEEE Symposium on Application Specific Processors, July 2009.

*   _Eliminating Microarchitectural Dependency from Architectural Vulnerability._ V. Sridharan, D. R. Kaeli. Proceedings of the 15th International Symposium on High-Performance Computer Architecture (HPCA-15), February 2009.
*   _Producing Wrong Data Without Doing Anything Obviously Wrong!_ T. Mytkowicz, A. Diwan, M. Hauswirth, P. F. Sweeney. Proceedings of the 14th international conference on Architectural support for programming languages and operating systems (ASPLOS). 2009.
*   _End-To-End Performance Forecasting: Finding Bottlenecks Before They Happen_ A. Saidi, N. Binkert, S. Reinhardt, T. Mudge. Proceedings of the 36th International Symposium on Computer Architecture (ISCA-36), June 2009.
*   _Fast Switching of Threads Between Cores._ R. Strong, J. Mudigonda, J. C. Mogul, N. Binkert, D. Tullsen. ACM SIGOPS Operating Systems Review. 2009.
*   _Express Cube Topologies for On-Chip Interconnects._ B. Grot, J. Hestness, S. W. Keckler, O. Mutlu. Proceedings of the 15th International Symposium on High-Performance Computer Architecture (HPCA-15), February 2009.
*   _Enhancing LTP-Driven Cache Management Using Reuse Distance Information._ W. Lieu, D. Yeung. Journal of Instruction-Level Parallelism 11 (2009).

## 2008<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2008"></span>

*   _Analyzing the Impact of Data Prefetching on Chip MultiProcessors._ N. Fukumoto, T. Mihara, K. Inoue, and K. Murakami. Asia-Pacific Computer Systems Architecture Conference. 2008.
*   _Historical Study of the Development of Branch Predictors._ Y. Peress. Masters Thesis at Florida State University. 2008.

*   _Hierarchical Domain Partitioning For Hierarchical Architectures._ J. Meng, S. Che, J. W. Sheaffer, J. Li, J. Huang, and K. Skadron. Univ. of Virginia Dept. of Comp. Sci. Tech Report CS-2008-08\. 2008.
*   _Memory Access Scheduling Schemes for Systems with Multi-Core Processors._ H. Zheng, J. Lin, Z. Zhang, and Z. Zhu. International Conference on Parallel Processing, 2008.

*   _Register Multimapping: Reducing Register Bank Conflicts Through One-To-Many Logical-To-Physical Register Mapping._ N. L. Duong and R. Kumar. Tehnical Report CHRC-08-07.
*   _Cross-Layer Custimization Platform for Low-Power and Real-Time Embedded Applications._ X. Zhou. Dissertation at the University of Maryland. 2008.
*   _Probabilistic Replacement: Enabling Flexible Use of Shared Caches for CMPs._ W. Liu and D. Yeung. University of Maryland Technical Report UMIACS-TR-2008-13\. 2008.
*   _Observer Effect and Measurement Bias in Performance Analysis_. T. Mytkowicz, P. F. Sweeney, M. Hauswirth, and A. Diwan. University of Colorado at Boulder Technical Report CU-CS 1042-08\. June, 2008.
*   _Power-Aware Dynamic Cache Partitioning for CMPs._ I. Kotera, K. Abe, R. Egawa, H. Takizawa, and H. Kobayashi. 3rd International Conference on High Performance and Embedded Architectures and Compilers (HiPEAC). 2008.
*   _Modeling of Cache Access Behavior Based on Zipf’s Law._ I. Kotera, H. Takizawa, R. Egawa, H. Kobayashi. MEDEA 2008.
*   _Hierarchical Verification for Increasing Performance in Reliable Processors._ J. Yoo, M. Franklin. Journal of Electronic Testing. 2008.

*   _Transaction-Aware Network-on-Chip Resource Reservation._ Z. Li, C. Zhu, L. Shang, R. Dick, Y. Sun. Computer Architecture Letters. Volume PP, Issue 99, Page(s):1 - 1.

*   _Predictable Out-of-order Execution Using Virtual Traces._ J. Whitham, N. Audsley. Proceedings of the 29th IEEE Real-time Systems Symposium, December 2008. [pdf](http://www.jwhitham.org.uk/pubs/vt1.pdf)

*   _Architectural and Compiler Mechanisms for Acelerating Single Thread Applications on Multicore Processors._ H. Zhong. Dissertation at The University of Michigan. 2008.

*   _Mini-Rank: Adaptive DRAM Architecture for Improving Memory Power Efficiency._ H. Zheng, J. Lin, Z. Zhang, E. Gorbatov, H. David, Z. Zhu. Proceedings of the 41st Annual Symposium on Microarchitecture (MICRO-41), November 2008.

*   _Reconfigurable Energy Efficient Near Threshold Cache Architectures._ R. Dreslinski, G. Chen, T. Mudge, D. Blaauw, D. Sylvester, K. Flautner. Proceedings of the 41st Annual Symposium on Microarchitecture (MICRO-41), November 2008.

*   _Distributed and low-power synchronization architecture for embedded multiprocessors._ C. Yu, P. Petrov. Internation Conference on Hardware/Software Codesign and System Synthesis (CODES+ISSS), October 2008.

*   _Thermal Monitoring Mechanisms for Chip Multiprocessors._ J. Long, S.O. Memik, G. Memik, R. Mukherjee. ACM Transactions on Architecture and Code Optimization (TACO), August 2008.

*   _Multi-optimization power management for chip multiprocessors._ K. Meng, R. Joseph, R. Dick, L. Shang. Proceedings of the 17th international conference on Parallel Architectures and Compilation Techniques (PACT), 2008.

*   ” Three-Dimensional Chip-Multiprocessor Run-Time Thermal Management.” C. Zhu, Z. Gu, L. Shang, R.P. Dick, R. Joseph. IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), August 2008.

*   ” Latency and bandwidth efficient communication through system customization for embedded multiprocessors”. C. Yu and P. Petrov. DAC 2008, June 2008.

*   _Corona: System Implications of Emerging Nanophotonic Technology_. D. Vantrease, R. Schreiber, M. Monchiero, M. McLaren, N., P. Jouppi, M. Fiorentino, A. Davis, N. Binkert, R. G. Beausoleil, and J. Ahn. Proceedings of the 35th International Symposium on Computer Architecture (ISCA-35), June 2008.

*   _Improving NAND Flash Based Disk Caches_. T. Kgil, D. Roberts and T. N. Mudge. Proceedings of the 35th International Symposium on Computer Architecture (ISCA-35), June 2008.

*   _A Taxonomy to Enable Error Recovery and Correction in Software_. V. Sridharan, D. A. Liberty, and D. R. Kaeli. Workshop on Quality-Aware Design (W-QUAD), in conjunction with the 35th International Symposium on Computer Architecture (ISCA-35), June 2008.

*   _Quantifying Software Vulnerability_. V. Sridharan and D. R. Kaeli. First Workshop on Radiation Effects and Fault Tolerance in Nanometer Technologies, in conjunction with the ACM International Conference on Computing Frontiers, May 2008.

*   _Core Monitors: Monitoring Performance in Multicore Processors._ P. West. Masters Thesis at Florida State University. April 2008.

*   _Full System Critical Path Analysis._ A. Saidi, N. Binkert, T. N. Mudge, and S. K. Reinhardt. 2008 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), April 2008.

*   _A Power and Temperature Aware DRAM Architecture._ S. Liu, S. O. Memik, Y. Zhang, G. Memik. 45th annual conference on Design automation (DAC), 2008.

*   _Streamware: Programming General-Purpose Multicore Processors Using Streams._ J. Gummaraju, J. Coburn, Y. Turner, M. Rosenblum. Procedings of the Thirteenth International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS), March 2008.

*   _Application-aware snoop filtering for low-power cache coherence in embedded multiprocessors_. X. Zhou, C. Yu, A. Dash, and P. Petrov. Transactions on Design Automation of Electronic Systems (TODAES). January 2008.

*   _An approach for adaptive DRAM temperature and power management_. Song Liu, S. O. Memik, Y. Zhang, and G. Memik. Proceedings of the 22nd annual international conference on Supercomputing. 2008.

## 2007<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2007"></span>

*   _Modeling and Characterizing Power Variability in Multicore Architectures._ K. Meng, F. Huebbers, R, Joseph, and Y. Ismail. ISPASS-2007.
*   _A High Performance Adaptive Miss Handling Architecture for Chip Multiprocessors._ M. Jahre, and L. Natvig. HiPEAC Journal 2007.
*   _Performance Effects of a Cache Miss Handling Architecture in a Multi-core Processor._ M. Jahre and L. Natvig. NIK-2007 conference. 2007.
*   _Prioritizing Verification via Value-based Correctness Criticality._ J. Yoo, M. Franklin. Proceedings of the 25th International Conference on Computer Design (ICCD), 2007.

*   _DRAM-Level Prefetching for Fully-Buffered DIMM: Design, Performance and Power Saving._ J. Lin, H. Zheng, Z. Zhu, Z. Zhang ,H. David. ISPASS 2007.

*   ” Virtual Exclusion: An architectural approach to reducing leakage energy in caches for multiprocessor systems”. M. Ghosh, H. Lee. Proceedings of the International Conference on Parallel and Distributed Systems. December 2007.

*   _Dependability-Performance Trade-off on Multiple Clustered Core Processors_. T. Funaki, T. Sato. Proceedings of the 4th International Workshop on Dependable Embedded Systems. October 2007.

*   _Predictive Thread-to-Core Assignment on a Heterogeneous Multi-core Processor_. T. Sondag, V. Krishnamurthy, H. Rajan. PLOS ‘07: ACM SIGOPS 4th Workshop on Programming Languages and Operating Systems. October 2007.

*   _Power deregulation: eliminating off-chip voltage regulation circuitry from embedded systems_. S. Kim, R. P. Dick, R. Joseph. 5th IEEE/ACM International Conference on Hardware/Software Co-Design and System Synthesis (CODES+ISSS). October 2007.

*   _Aggressive Snoop Reduction for Synchronized Producer-Consumer Communication in Energy-Efficient Embedded Multi-Processors_. C. Yu, P. Petrov. 5th IEEE/ACM International Conference on Hardware/Software Co-Design and System Synthesis (CODES+ISSS). October 2007.

*   _Three-Dimensional Multiprocessor System-on-Chip Thermal Optimization_. C. Sun, L. Shang, R.P. Dick. 5th IEEE/ACM International Conference on Hardware/Software Co-Design and System Synthesis (CODES+ISSS). October 2007.

*   _Sampled Simulation for Multithreaded Processors_. M. Van Biesbrouck. (Thesis) UC San Diego Technical Report CS2007-XXXX. September 2007.

*   _Representative Multiprogram Workloads for Multithreaded Processor Simulation_. M. Van Biesbroucky, L. Eeckhoutz, B. Calder. IEEE International Symposium on Workload Characterization (IISWC). September 2007.

*   _The Interval Page Table: Virtual Memory Support in Real-Time and Memory-Constrained Embedded Systems_. X. Zhou, P. Petrov. Proceedings of the 20th annual conference on Integrated circuits and systems design. 2007.

*   _A power-aware shared cache mechanism based on locality assessment of memory reference for CMPs_. I. Kotera, R. Egawa, H. Takizawa, H. Kobayashi. Proceedings of the 2007 workshop on MEmory performance: DEaling with Applications, systems and architecture (MEDEA). September 2007.

*   _Architectural Support for the Stream Execution Model on General-Purpose Processors_. J. Gummaraju, M. Erez, J. Coburn, M. Rosenblum, W. J. Dally. The Sixteenth International Conference on Parallel Architectures and Compilation Techniques (PACT). September 2007.

*   _An Energy Efficient Parallel Architecture Using Near Threshold Operation_. R. Dreslinski, B. Zhai, T. Mudge, D. Blaauw, D. Sylvester. The Sixteenth International Conference on Parallel Architectures and Compilation Techniques (PACT). September 2007.

*   _When Homogeneous becomes Heterogeneous: Wearout Aware Task Scheduling for Streaming Applications_. D. Roberts, R. Dreslinski, E. Karl, T. Mudge, D. Sylvester, D. Blaauw. Workshop on Operationg System Support for Heterogeneous Multicore Architectures (OSHMA). September 2007.

*   ” On-Chip Cache Device Scaling Limits and Effective Fault Repair Techniques in Future Nanoscale Technology”. D. Roberts, N. Kim,T. Mudge. Digital System Design Architectures, Methods and Tools (DSD). August 2007.

*   _Energy Efficient Near-threshold Chip Multi-processing_. B. Zhai, R. Dreslinski, D. Blaauw, T. Mudge, D. Sylvester. International Symposium on Low Power Electronics and Design (ISLPED). August 2007.

*   ” A Burst Scheduling Access Reordering Mechanism”. J. Shao, B.T. Davis. IEEE 13th International Symposium on High Performance Computer Architecture (HPCA). 2007.

*   _Enhancing LTP-Driven Cache Management Using Reuse Distance Information_. W. Liu, D. Yeung. University of Maryland Technical Report UMIACS-TR-2007-33\. June 2007.

*   _Thermal modeling and management of DRAM memory systems_. J. Lin, H. Zheng, Z. Zhu, H. David, and Z. Zhang. Proceedings of the 34th Annual international Symposium on Computer Architecture (ISCA). June 2007.

*   _Duplicating and Verifying LogTM with OS Support in the M5 Simulator_. G. Blake, T. Mudge. Sixth Annual Workshop on Duplicating, Deconstructing, and Debunking (WDDD). June 2007.

*   _Analysis of Hardware Prefetching Across Virtual Page Boundaries_. R. Dreslinski, A. Saidi, T. Mudge, S. Reinhardt. Proc. of the 4th Conference on Computing Frontiers. May 2007.

*   _Reliability in the Shadow of Long-Stall Instructions_. V. Sridharan, D. Kaeli, A. Biswas. Third Workshop on Silicon Errors in Logic - System Effects (SELSE-3). April 2007.

*   _Extending Multicore Architectures to Exploit Hybrid Parallelism in Single-thread Applications_. H. Zhong, S. A. Lieberman, S. A. Mahlke. Proc. 13th Intl. Symposium on High Performance Computer Architecture (HPCA). February 2007.

## 2006<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2006"></span>

*   _Evaluation of the Data Vortex Photonic All-Optical Path Interconnection Network for Next-Generation Supercomputers_. W. C. Hawkins. Dissertation at Georgia Tech. December 2006.

*   _Running the manual: an approach to high-assurance microkernel development_. P. Derrin, K. Elphinstone, G. Klein, D. Cock, M. M. T. Chakravarty. Proceedings of the 2006 ACM SIGPLAN workshop on Haskell. 2006.

*   _The Filter Checker: An Active Verification Management Approach_. J. Yoo, M. Franklin. 21st IEEE International Symposium on Defect and Fault-Tolerance in VLSI Systems (DFT’06), 2006.

*   _Physical Resource Matching Under Power Asymmetry_. K. Meng, F. Huebbers, R. Joseph, Y. Ismail. Presented at the 2006 P=ac2 Conference. 2006. [pdf](http://www.ece.northwestern.edu/~rjoseph/publications/man-asymmetry.pdf)

*   _Process Variation Aware Cache Leakage Management_. K. Meng, R. Joseph. Proceedings of the 2006 International Symposium on Low Power Electronics and Design (ISLPED). October 2006.

*   _FlashCache: a NAND flash memory file cache for low power web servers_. T. Kgil, T. Mudge. Proceedings of the 2006 international conference on Compilers, Architecture and Synthesis for Embedded Systems (CASES). October 2006.

*   _PicoServer: Using 3D Stacking Technology To Enable A Compact Energy Efficient Chip Multiprocessor_. T. Kgil, S. D’Souza, A. Saidi, N. Binkert, R. Dreslinski, S. Reinhardt, K. Flautner, T. Mudge. 12th Int’l Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS). October 2006.

*   _Integrated Network Interfaces for High-Bandwidth TCP/IP_. N. L. Binkert, A. G. Saidi, S. K. Reinhardt. 12th Int’l Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS). October 2006.

*   _Communist, utilitarian, and capitalist cache policies on CMPs: caches as a shared resource_. L. R. Hsu, S. K. Reinhardt, R. Iyer, S. Makineni. Proc. 15th Int’l Conf. on Parallel Architectures and Compilation Techniques (PACT), September 2006.

*   _Impact of CMP Design on High-Performance Embedded Computing_. P. Crowley, M. A. Franklin, J. Buhler, and R. D. Chamberlain. Proc. of 10th High Performance Embedded Computing Workshop. September 2006.

*   _BASS: A Benchmark suite for evaluating Architectural Security Systems_. J. Poe, T. Li. ACM SIGARCH Computer Architecture News. Vol. 34, No. 4, September 2006.

*   _The M5 Simulator: Modeling Networked Systems_. N. L. Binkert, R. G. Dreslinski, L. R. Hsu, K. T. Lim, A. G. Saidi, S. K. Reinhardt. IEEE Micro, vol. 26, no. 4, pp. 52-60, July/August, 2006.[Link](http://csdl2.computer.org/persagen/DLAbsToc.jsp?resourcePath=/dl/mags/mi/&toc=comp/mags/mi/2006/04/m4toc.xml&DOI=10.1109/MM.2006.82)

*   _Considering All Starting Points for Simultaneous Multithreading Simulation_. M. Van Biesbrouck, L. Eeckhout, B. Calder. Proc. of the Int’l Symp. on Performance Analysis of Systems and Software (ISPASS). 2006.[pdf](http://www.cse.ucsd.edu/users/calder/papers/ISPASS-06-CoPhaseAllPairs.pdf)

*   _Dynamic Thread Assignment on Heterogeneous Multiprocessor Architectures_. M. Becchi, P. Crowley. Proc. of the 3rd Conference on Computing Frontiers. pp29-40\. May 2006. [pdf](http://portal.acm.org/ft_gateway.cfm?id=1128029&type=pdf&coll=GUIDE&dl=GUIDE&CFID=15151515&CFTOKEN=6184618)

*   _Integrated System Architectures for High-Performance Internet Servers_. N. L. Binkert. Dissertation at the University of Michigan. February 2006.

*   _Exploring Salvage Techniques for Multi-core Architectures_. R. Joseph. 2nd Workshop on High Performance Computing Reliability Issues. February 2006. [pdf](http://www.ece.northwestern.edu/~rjoseph/publications/hpcri-salvage.pdf)

*   _A Simple Integrated Network Interface for High-Bandwidth Servers_. N. L. Binkert, A. G. Saidi, S. K. Reinhardt. University of Michigan Technical Report CSE-TR-514-06, January 2006. [pdf](http://www.eecs.umich.edu/techreports/cse/2006/CSE-TR-514-06.pdf)

## 2005<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2005"></span>

*   _Software Defined Radio - A High Performance Embedded Challenge_. H. lee, Y. Lin, Y. Harel, M. Woh, S. Mahlke, T. Mudge, K. Flautner. Proc. 2005 Int’l Conf. on High Performance Embedded Architectures and Compilers (HiPEAC). November 2005. [pdf](http://www.eecs.umich.edu/~sdrg/lee-hipeac05.pdf)

*   _How to Fake 1000 Registers_. D. W. Oehmke, N. L. Binkert, S. K. Reinhardt, and T. Mudge. Proc. 38th Ann. Int’l Symp. on Microarchitecture (MICRO), November 2005. [pdf](http://www.eecs.umich.edu/~stever/pubs/micro05.pdf)

*   _Virtualizing Register Context_. D. W. Oehmke. Dissertation at the University of Michigan, 2005. [pdf](http://www.eecs.umich.edu/~tnm/theses/davidO.pdf)

*   _Performance Validation of Network-Intensive Workloads on a Full-System Simulator_. A. G. Saidi, N. L. Binkert, L. R. Hsu, and S. K. Reinhardt. First Ann. Workshop on Iteraction between Operating System and Computer Architecture (IOSCA), October 2005. [pdf](http://www.eecs.umich.edu/~stever/pubs/iosca05.pdf)
    *   An extended version appears as University of Michigan Technical Report CSE-TR-511-05, July 2005. [pdf](http://www.eecs.umich.edu/techreports/cse/2005/CSE-TR-511-05.pdf)

*   _Performance Analysis of System Overheads in TCP/IP Workloads_. N. L. Binkert, L. R. Hsu, A. G. Saidi, R. G. Dreslinski, A. L. Schultz, and S. K. Reinhardt. Proc. 14th Int’l Conf. on Parallel Architectures and Compilation Techniques (PACT), September 2005. [pdf](http://www.eecs.umich.edu/~stever/pubs/pact05.pdf)

*   _Sampling and Stability in TCP/IP Workloads_. L. R. Hsu, A. G. Saidi, N. L. Binkert, and S. K. Reinhardt. Proc. First Annual Workshop on Modeling, Benchmarking, and Simulation (MoBS), June
    1.  [pdf](http://www.eecs.umich.edu/~stever/pubs/mobs05.pdf)

*   _A Unified Compressed Memory Hierarchy_. E. G. Hallnor and S. K. Reinhardt. Proc. 11th Int’l Symp. on High-Performance Computer Architecture (HPCA), February 2005. [pdf](http://www.eecs.umich.edu/~stever/pubs/hpca05.pdf)

*   _Analyzing NIC Overheads in Network-Intensive Workloads_. N. L. Binkert, L. R. Hsu, A. G. Saidi, R. G. Dreslinski, A. L. Schultz, and S. K. Reinhardt. Eighth Workshop on Computer Architecture Evaluation using Commercial Workloads (CAECW), February 2005. [pdf](http://tesla.hpl.hp.com/caecw05/binkert-caecw8.pdf)
    *   An extended version appears as University of Michigan Technical Report CSE-TR-505-04, December 2004. [pdf](http://www.eecs.umich.edu/techreports/cse/2004/CSE-TR-505-04.pdf)

## 2004<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2004"></span>

*   _Emulation of realisitic network traffic patterns on an eight-node data vortex interconnection network subsytem_. B. Small, A. Shacham, K. Bergman, K. Athikulwongse, C. Hawkins, and D.S. Will. Journal of Optical Networking Vol. 3, No.11, pp 802-809, November 2004. [pdf](http://lightwave.ee.columbia.edu/files/Small2004.pdf)

*   _ChipLock: Support for Secure Microarchitectures_. T. Kgil, L Falk, and T. Mudge. Proc. Workshop on Architectural Support for Security and Anti-virus (WASSA), October 2004, pp. 130-139. [pdf](http://www.eecs.umich.edu/~tnm/papers/wassa04.pdf)

*   _Design and Applications of a Virtual Context Architecture_. D. Oehmke, N. Binkert, S. Reinhardt, and T. Mudge. University of Michigan Technical Report CSE-TR-497-04, September 2004. [pdf](http://www.eecs.umich.edu/techreports/cse/2004/CSE-TR-497-04.pdf)

*   _The Performance Potential of an Integrated Network Interface_. N. L. Binkert, R. G. Dreslinski, E. G. Hallnor, L. R. Hsu, S. E. Raasch, A. L. Schultz, and S. K. Reinhardt. Proc. Advanced Networking and Communications Hardware Workshop (ANCHOR), June 2004. [pdf](http://www.eecs.umich.edu/~stever/pubs/anchor04.pdf)

*   _A Co-Phase Matrix to Guide Simultaneous Multithreading Simulation_. M. Van Biesbrouck, T. Sherwood, and B. Calder. IEEE International Symposium on Performance Analysis and Software (ISPASS), March 2004. [pdf](http://www.cs.ucsd.edu/~calder/papers/ISPASS-04-CoPhaseMatrix.pdf)

*   _A Compressed Memory Hierarchy using an Indirect Index Cache_. E. G. Hallnor and S. K. Reinhardt. Proc. 3rd Workshop on Memory Performance Issues (WMPI), June 2004. [pdf](http://www.eecs.umich.edu/~stever/pubs/wmpi04.pdf)
    *   An extended version appears as University of Michigan Technical Report CSE-TR-488-04, March 2004. [pdf](http://www.eecs.umich.edu/techreports/cse/2004/CSE-TR-488-04.pdf)

## 2003<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2003"></span>

*   _The Impact of Resource Partitioning on SMT Processors_. S. E. Raasch and S. K. Reinhardt. Proc. 12th Int’l Conf. on Parallel Architectures and Compilation Techniques (PACT), pp. 15-25, Sept.
    1.  [pdf](http://www.eecs.umich.edu/~stever/pubs/pact03.pdf)

*   _Network-Oriented Full-System Simulation using M5_. N. L. Binkert, E. G. Hallnor, and S. K. Reinhardt. Sixth Workshop on Computer Architecture Evaluation using Commercial Workloads (CAECW), February
    1.  [pdf](http://www.eecs.umich.edu/~stever/pubs/caecw03.pdf)

*   _Design, Implementation and Use of the MIRV Experimental Compiler for Computer Architecture Research_. D. A. Greene. Dissertation at the Universtiy of Michigan, 2003. [[http://www.eecs.umich.edu/~tnm/theses/daveg.pdg](http://www.eecs.umich.edu/~tnm/theses/daveg.pdg)“>pdf ]

## 2002<span class="anchor" data-clipboard-text="http://www.gem5.org/publications/#2002"></span>

*   _A Scalable Instruction Queue Design Using Dependence Chains_. S. E. Raasch, N. L. Binkert, and S. K. Reinhardt. Proc. 29th Annual Int’l Symp. on Computer Architecture (ISCA), pp. 318-329, May 2002. [pdf](http://www.eecs.umich.edu/~stever/pubs/isca02_segiq.pdf) [ps](http://www.eecs.umich.edu/~stever/pubs/isca02_segiq.ps) [ps.gz](http://www.eecs.umich1111/~stever/pubs/isca02_segiq.ps.gz)
