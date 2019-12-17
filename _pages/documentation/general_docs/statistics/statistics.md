---
layout: documentation
title: Statistics
parent: statistics
doc: gem5 documentation
permalink: /documentation/general_docs/statistics/
---

# Stats Package
The philosophy of the stats package at the moment is to have a single base class called Stat which is merely a hook into every other aspect of the stat that may be important. Thus, this Stat base class has virtual functions to name, set precision for, set flags for, and initialize size for all the stats. For all Vector based stats, it is very important to do the initialization before using the stat so that appropriate storage allocation can occur. For all other stats, naming and flag setting is also important, but not as important for the actual proper execution of the binary. The way this is set up in the code is to have a regStats() pass in which all stats can be registered in the stats database and initialized.

Thus, to add your own stats, just add them to the appropriate class' data member list, and be sure to initialize/register them in that class' regStats function.

Here is a list of the various initialization functions. Note that all of these return a Stat& reference, thus enabling a clean looking way of calling them all.

* init(various args) //this differs for different types of stats.
   * Average: does not have an init()
   * Vector: init(size_t) //indicates size of vector
   * AverageVector: init(size_t) //indicates size of vector
   * Vector2d: init(size_t x, size_t y) //rows, columns
   * Distribution: init(min, max, bkt) //min refers to minimum value, max the maximum value, and bkt the size of the bkts. In other words, if you have min=0, max=15, and bkt=8, then 0-7 will go into bucket 0, and 8-15 will go into bucket 1.
   * StandardDeviation: does not have an init()
   * AverageDeviation: does not have an init()
   * VectorDistribution: init(size, min, max, bkt) //the size refers to the size of the vector, the rest are the same as for Distributions.
   * VectorStandardDeviation: init(size) //size refers to size of the vector
   * VectorAverageDeviation: init(size) //size refers to size of the vector
   * Formula: does not have an init()
* name(const std::string name) //the name of the stat
* desc(const std::string desc) //a brief description of the stat
* precision(int p) //p refers to how many places after the decimal point to go. p=0 will force rounding to integers.
* prereq(const Stat &prereq) //this indicates that this stat should not be printed unless prereq has a non-zero value. (like if there are 0 cache accesses, don't print cache misses, hits, etc.)
* subname(int index, const std::string subname) //this is for Vector based stats to give a subname to each index of the vector.
* subdesc(int index, const std::string subname) //also for Vector based stats, to give each index a subdesc. For 2d Vectors, the subname goes to each of the rows (x's). The y's can be named using a Vector2d member function ysubname, see code for details.

flags(FormatFlags f) //these are various flags you can pass to the stat, which i'll describe below.

* none -- no special formatting
* total -- this is for Vector based stats, if this flag is set, the total across the Vector will be printed at the end (for those stats which this is supported).
* pdf -- This will print the probability distribution of a stat
* nozero -- This will not print the stat if its value is zero
* nonan -- This will not print the stat if it's Not a Number (nan).
* cdf -- This will print the cumulative distribution of a stat

Below is an example of how to initialize a VectorDistribution:

```
    vector_dist.init(4,0,5,2)
        .name("Dummy Vector Dist")
        .desc("there are 4 distributions with buckets 0-1, 2-3, 4-5")
        .flags(nonan | pdf)
        ;
```
# Stat Types #
## Scalar ## 
The most basic stat is the Scalar. This embodies the basic counting stat. It is a templatized stat and takes two parameters, a type and a bin. The default type is a Counter, and the default bin is NoBin (i.e. there is no binning on this stat). It's usage is straightforward: to assign a value to it, just say foo = 10;, or to increment it, just use ++ or += like for any other type.
## Average ##
This is a "special use" stat, geared toward calculating the average of something over the number of cycles in the simulation. This stat is best explained by example. If you wanted to know the average occupancy of the load-store queue over the course of the simulation, you'd need to accumulate the number of instructions in the LSQ each cycle and at the end divide it by the number of cycles. For this stat, there may be many cycles where there is no change in the LSQ occupancy. Thus, you could use this stat, where you only need to explicitly update the stat when there is a change in the LSQ occupancy. The stat itself will take care of itself for cycles where there is no change. This stat can be binned and it also templatized the same way Stat is.
## Vector ##
A Vector is just what it sounds like, a vector of type T in the template parameters. It can also be binned. The most natural use of Vector is for something like tracking some stat over number of SMT threads. A Vector of size n can be declared just by saying Vector<> foo; and later initializing the size to n. At that point, foo can be accessed as if it were a regular vector or array, like foo[7]++.
## AverageVector ##
An AverageVector is just a Vector of Averages.
## Vector2d ##
A Vector2d is a 2 dimensional vector. It can be named in both the x and y directions, though the primary name is given across the x-dimension. To name in the y-dimension, use a special ysubname function only available to Vector2d's.
## Distribution ##
This is essentially a Vector, but with minor differences. Whereas in a Vector, the index maps to the item of interest for that bucket, in a Distribution you could map different ranges of interest to a bucket. Basically, if you had the bkt parameter of init for a Distribution = 1, you might as well use a Vector.
## StandardDeviation ##
This stat calculates standard deviation over number of cycles in the simulation. It's similar to Average in that it has behavior built into it, but it needs to be updated every cycle.
## AverageDeviation ##
This stat also calculates the standard deviation but it does not need to be updated every cycle, much like Average. It will handle cycles where there is no change itself.
## VectorDistribution ##
This is just a vector of distributions.
## VectorStandardDeviation ##
This is just a vector of standard deviations.
## VectorAverageDeviation ##
This is just a vector of AverageDeviations.
## Histogram ##
This stat puts each sampled value into one bin out of a configurable number of bins. All bins form a contiguous interval and are of equal length. The length of the bins is dynamically extended, if there is a sample value which does not fit into one the existing bins.
## SparseHistogram ##
This stat is similar to a histogram, except that it can only sample natural numbers. SparseHistogram is e.g. suitable for counting the number of accesses to memory addresses.
## Formula ##
This is a Formula stat. This is for anything that requires calculations at the end of the simulation, for example something that is a rate. So, an example of defining a Formula would be:

```
    Formula foo = bar + 10 / num;
```

There are a few subtleties to Formula. If bar and num are both stats(including Formula type), then there is no problem. If bar or num are regular variables, then they must be qualified with constant(bar). This is essentially cast. If you want to use the value of bar or num at the moment of definition, then use constant(). If you want to use the value of bar or num at the moment the formula is calculated (i.e. the end), define num as a Scalar. If num is a Vector, use sum(num) to calculate its sum for the formula. The operation "scalar(num)", which casts a regular variable to a Scalar, does no longer exist.
