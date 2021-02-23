---
layout: documentation
title: Statistics API
parent: statistics
doc: gem5 documentation
permalink: /documentation/general_docs/statistics/api
---

# Statistics APIs

## Contents
1. [General Statistics Functions](#general-statistics-functions)
2. [Stats::Group - Statistics Container](#stats_group-statistics-container)
3. [Stats Flags](#stats-flags)
4. [Statistic Classes](#statistics-classes)
5. [Appendix: Migrating to the new style of tracking statistics](#appendix_migrating-to-the-new-style-of-tracking-statistics)

---

## General Statistics Functions

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void Stats::dump()`                                 | Dump all stats to registered outputs, e.g. stats.txt.                  |
|`void Stats::reset()`                                | Reset stats.                                                           |

---

## Stats::Group - Statistics Container
Typically, a statistic object can be placed in any `SimObject` as a class variable.
However, [a recent update](https://gem5-review.googlesource.com/c/public/gem5/+/19368)
addresses the hierarchical nature of `SimObject` 's in gem5,
which in turns makes the statistics of the objects hierarchical.
The update introduces the `Stats::Group` class, which is a statistics container
and is aware of the hierarchical structure of `SimObject`'s.
Ideally, this container should contain all stats in a `SimObject`.

**Note**: If you decide to use a `Stats::Group` struct inside of a `SimObject`,
there are typically two ways of doing this:
- Create a subgroup using `Stats::Group(Stats::Group &parent, const std::string &name)` constructor. This is useful when it is desired to have multiple instances of the same stats structure.
- Using `Stats::Group(Stats::Group &parent)` constructor, which merges (i.e. adds) the stats of the current group to the parent group. Thus, the stats added to the current group behave as if they were added to the parent group.

### Stats::Group macros
##### `#define ADD_STAT(n, ...) n(this, # n, __VA_ARGS__)`
Convenience macro to add a stat to a statistics group.

This macro is used to add a stat to a Stats::Group in the
initilization list in the Group's constructor. The macro
automatically assigns the stat to the current group and gives it
the same name as in the class. For example:
```
struct MyStats : public Stats::Group
{
    Stats::Scalar scalar0;
    Stats::Scalar scalar1;

    MyStats(Stats::Group *parent)
        : Stats::Group(parent),
          ADD_STAT(scalar0, "Description of scalar0"),       // equivalent to scalar0(this, "scalar0", "Description of scalar0"), where scalar0 has the follwing constructor
                                                             // Stats::Scalar(Group *parent = nullptr, const char *name = nullptr, const char *desc = nullptr)
          scalar1(this, "scalar1", "Description of scalar1")
     {
     }
};
```


### Stats::Group functions
##### `Group(Group *parent, const char *name = nullptr)`
Construct a new statistics group.

The constructor takes two parameters, a parent and a name. The
parent group should typically be specified. However, there are
special cases where the parent group may be null. One such
special case is SimObjects where the Python code performs late
binding of the group parent.

If the name parameter is NULL, the group gets merged into the
parent group instead of creating a sub-group. Stats belonging
to a merged group behave as if they have been added directly to
the parent group.

##### `virtual void regStats()`
Callback to set stat parameters.

This callback is typically used for complex stats (e.g.,
distributions) that need parameters in addition to a name and a
description. In the case stats objects cannot be initilalized
in the constructor (such as the stats that keep track of the
bus masters, which only can be discovered after the entire
system is instantiated). Stat names and descriptions should
typically be set from the constructor using the `ADD_STAT` macro.

##### `virtual void resetStats()`
Callback to reset stats.

##### `virtual void preDumpStats()`
Callback before stats are dumped. This can be overridden by
objects that need to perform calculations in addition to the
capabiltiies implemented in the stat framework.

##### `void addStat(Stats::Info *info)`
Register a stat with this group. This method is normally called
automatically when a stat is instantiated.

##### `const std::map<std::string, Group *> &getStatGroups() const`
Get all child groups associated with this object.

##### `const std::vector<Info *> &getStats() const`
Get all stats associated with this object.

##### `void addStatGroup(const char *name, Group *block)`
Add a stat block as a child of this block.

This method may only be called from a Group constructor or from
regStats. It's typically only called explicitly from Python
when setting up the SimObject hierarchy.

##### `const Info * resolveStat(std::string name) const`
Resolve a stat by its name within this group.

This method goes through the stats in this group and sub-groups
and returns a pointer to the the stat that matches the provided
name. The input name has to be relative to the name of this
group.

For example, if this group is the `SimObject
system.bigCluster.cpus` and we want the stat
`system.bigCluster.cpus.ipc`, the input param should be the
string "ipc".

---

## Stats Flags

| Flags            | Descriptions                                                   |
|------------------|----------------------------------------------------------------|
| `Stats::none`    | Nothing extra to print.                                        |
| `Stats::total`   | Print the total.                                               |
| `Stats::pdf`     | Print the percent of the total that this entry represents.     |
| `Stats::cdf`     | Print the cumulative percentage of total upto this entry.      |
| `Stats::dist`    | Print the distribution.                                        |
| `Stats::nozero`  | Don't print if this is zero.                                   |
| `Stats::nonan`   | Don't print if this is NAN                                     |
| `Stats::oneline` | Print all values on a single line. Useful only for histograms. |

Note: even though the flags `Stats::init` and `Stats::display` are available, the flags
are not allowed to be set by users.

---

## Statistics Classes

| Class names                                         | Descriptions                                                            |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| [`Stats::Scalar`](#statsscalar)                     | Simple scalar statistic.                                                |
| [`Stats::Average`](#statsaverage)                   | A statistic that calculate the PER TICK average of a value.             |
| [`Stats::Value`](#statsvalue)                       | Similar to Stats::Scalar.                                               |
| [`Stats::Vector`](#statsvector)                     | A vector of scalar statistics.                                          |
| [`Stats::AverageVector`](#statsaveragevector)       | A vector of average statistics.                                         |
| [`Stats::Vector2d`](#statsvector2d)                 | A 2D vector of scalar statistics.                                       |
| [`Stats::Distribution`](#statsdistribution)         | A simple distribution statistic (having convinient min, max sum, etc.). |
| [`Stats::Histogram`](#statshistogram)               | A simple histogram statistic (keeping the frequencies of equally-splitted continuous ranges). |
| [`Stats::SparseHistogram`](#statssparsehistogram)   | Keeps the frequency / histogram of a collection of discrete values.     |
| [`Stats::StandardDeviation`](#statsstandarddeviation)| Calculates the mean and variance of all samples.                       |
| [`Stats::AverageDeviation`](#statsaveragedeviation) | Calculates per tick mean and variance of samples.                       |
| [`Stats::VectorDistribution`](#statsvectordistribution)| A vector of distributions.                                           |
| [`Stats::VectorStandardDeviation`](#statsvectorstandarddeviation)| A vector of standard deviation statistics.                 |
| [`Stats::VectorAverageDeviation`](#statsvectoraveragedeviation)| A vector of average deviation statistics.                    |
| [`Stats::Formula`](#statsformula)                   | Keeps the statistic involving arithmetics of multiple stats objects.    |

**Note:** `Stats::Average` only calculates the average of a scalar over the number of simulated ticks.
In order to get the average of quantity A over quantity B, `Stats::Formula` can be utilized.
For example,
```C++
Stats::Scalar totalReadLatency;
Stats::Scalar numReads;
Stats::Formula averageReadLatency = totalReadLatency/numReads;
```

### Common statistic functions

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`StatClass name(const std::string &name)`            | sets the statistic name, marks the stats to be printed                 |
|`StatClass desc(const std::string &_desc)`           | sets the description for the statistic                                 |
|`StatClass precision(int _precision)`                | sets the precision of the statistic                                    |
|`StatClass flags(Flags _flags)`                      | sets the flags                                                         |
|`StatClass prereq(const Stat &prereq)`               | sets the prerequisite stat                                             |

### `Stats::Scalar`
Storing a signed integer statistic.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void operator++()`                                  | increments the stat by 1 // prefix ++, e.g. `++scalar`                 |
|`void operator--()`                                  | decrements the stat by 1 // prefix --                                  |
|`void operator++(int)`                               | increments the stat by 1 // postfix ++, e.g. `scalar++`                |
|`void operator--(int)`                               | decrements the stat by 1 // postfix --                                 |
|`template <typename U> void operator=(const U &v)`   | sets the scalar to the given value                                     |
|`template <typename U> void operator+=(const U &v)`  | increments the stat by the given value                                 |
|`template <typename U> void operator-=(const U &v)`  | decrements the stat by the given value                                 |
|`size_type size()`                                   | returns 1                                                              |
|`Counter value()`                                    | returns the current value of the stat as an integer                    |
|`Counter value() const`                              | returns the current value of the stat as an integer                    |
|`Result result()`                                    | returns the current value of the stat as a `double`                    |
|`Result total()`                                     | returns the current value of the stat as a `double`                    |
|`bool zero()`                                        | returns `true` if the stat equals to zero, returns `false` otherwise   |
|`void reset()`                                       | resets the stat to 0                                                   |

### `Stats::Average`
Storing an average of an integer quantity, supposely A, over the number of simulated ticks.
The quantity A keeps the same value across all ticks after its latest update and before the next update.
**Note:** the number of simulated ticks is reset when the user calls `Stats::reset()`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void set(Counter val)`                              | sets the quantity A to the given value                                 |
|`void inc(Counter val)`                              | increments the quantity A by the given value                           |
|`void dec(Counter val)`                              | decrements the quantity A by the given value                           |
|`Counter value()`                                    | returns the current value of A as an integer                           |
|`Result result()`                                    | returns the current average as a `double`                              |
|`bool zero()`                                        | returns `true` if the average equals to zero, returns `false` otherwise|
|`void reset(Info \*info)`                            | keeps the current value of A, does not count the value of A before the current tick|

### `Stats::Value`
Storing a signed integer statistic that is either an integer or an integer that is a result from calling a function or an object's method.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Counter value()`                                    | returns the value as an integer                                        |
|`Result result() const`                              | returns the value as a double                                          |
|`Result total() const`                               | returns the value as a double                                          |
|`size_type size() const`                             | returns 1                                                              |
|`bool zero() const`                                  | returns `true` if the value is zero, returns `false` otherwise         |


### `Stats::Vector`
Storing an array of scalar statistics where each element of the vector has function signatures similar to those of `Stats::Scalar`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type size)`                     | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                 |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index          |
|`void value(VCounter &vec) const`                    | copies the vector of statistics to the given vector of integers        |
|`void result(VResult &vec) const`                    | copies the vector of statistics to the given vector of doubles         |
|`Result total() const`                               | returns the sum of all statistics in the vector as a double            |
|`size_type size() const`                             | returns the size of the vector                                         |
|`bool zero() const`                                  | returns `true` if each statistic in the vector is 0, returns `false` otherwise|
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `vecStats[1]+=9`|

### `Stats::AverageVector`
Storing an array of average statistics where each element of the vector has function signatures similar to those of `Stats::Average`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type size)`                     | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                 |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index          |
|`void value(VCounter &vec) const`                    | copies the vector of statistics to the given vector of integers        |
|`void result(VResult &vec) const`                    | copies the vector of statistics to the given vector of doubles         |
|`Result total() const`                               | returns the sum of all statistics in the vector as a double            |
|`size_type size() const`                             | returns the size of the vector                                         |
|`bool zero() const`                                  | returns `true` if each statistic in the vector is 0, returns `false` otherwise|
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `avgStats[1].set(9)`|

### `Stats::Vector2d`
Storing a 2-dimensional array of scalar statistics, where each element of the array has function signatures similar to those of `Stats::Scalar`.
This data structure assumes all elements whose the same second dimension index has the same name.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type _x, size_type _y)`         | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & ysubname(off_type index, const std::string &subname)` | sets `subname` as the name of the statistics of elements whose the second dimension of `index`|
|`Derived & ysubnames(const char **names)`            | similar to `ysubname()` above, but sets name for all indices of the second dimension|
|`std::string ysubname(off_type i) const`             | returns the name of the statistics of elements whose the second dimension of `i`|
|`size_type size() const`                             | returns the number of elements in the array                            |
|`bool zero()`                                        | returns `true` if the element at row 0 column 0 equals to 0, returns `false` otherwise |
|`Result total()`                                     | returns the sum of all elements as a double
|`void reset()`                                       | sets each element in the array to 0                                    |
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `vecStats[1][2]+=9`|

### `Stats::Distribution`
Storing a distribution of a quantity.
The statistics of the distribution include,
  - the smallest/largest value being sampled
  - the number of values that are smaller/larger than the specified minimum and maximum
  - the sum of all samples
  - the mean, the geometric mean and the standard deviation of the samples
  - histogram within the range of [`min`, `max`] splitted into `(max-min)/bucket_size` equally sized buckets,  where the `min`/`max`/`bucket_size` are inputs to the init() function.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`Distribution & init(Counter min, Counter max, Counter bkt)` | initializes the distribution where `min` is the minimum value being tracked by the distribution's histogram, `max` is the minimum value being tracked by the distribution's histogram, and `bkt` is the number of values in each bucket |
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns the number of bucket in the distribution                       |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset(Info *info)`                                     | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Histogram`)|

### `Stats::Histogram`
Storing a histogram of a quantity given the number of buckets.
All buckets are equally sized.
Different from the histogram of `Stats::Distribution` which keeps track of the samples in a specific range, `Stats::Histogram` keeps track of all samples in its histogram.
Also, while `Stats::Distribution` is parameterized by the number of values in a bucket, `Stats::Histogram`'s sole parameter is the number of buckets.
When a new sample is outside of the current range of all all buckets, the buckets will be resized.
Roughly, two consecutive buckets will be merged until the new sample is inside one of the buckets.

Other than the histogram itself, the statistics of the distribution include,
  - the smallest/largest value being sampled
  - the sum of all samples
  - the mean, the geometric mean and the standard deviation of the samples

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`Histogram & init(size_type size)`                           | initializes the histogram, sets the number of buckets to `size`        |
|`void sample(Counter val, int number)`                       | adds `val` to the histogram `number` times                             |
|`void add(HistStor *)`                                       | merges another histogram to this histogram                             |
|`size_type size() const `                                    | returns the number of buckets                                          |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset(Info *info)`                                     | discards all samples                                                   |

### `Stats::SparseHistogram`
Storing a histogram of a quantity given a set of integral values.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`template <typename U> void sample(const U &v, int n = 1)`   | adds `v` to the histogram `n` times                                    |
|`size_type size() const `                                    | returns the number of entries                                          |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset()`                                               | discards all samples                                                   |

### `Stats::StandardDeviation`
Keeps track of the standard deviation of a sample.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns 1                                                              |
|`bool zeros() const`                                         | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Distribution`|

### `Stats::AverageDeviation`
Keeps track of the average deviation of a sample.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns 1                                                              |
|`bool zeros() const`                                         | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Distribution`|

### `Stats::VectorDistribution`
Storing a vector of distributions where each element of the vector has function signatures similar to those of `Stats::Distribution`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorDistribution & init(size_type size, Counter min, Counter max, Counter bkt)` | initializes a vector of `size` distributions where `min` is the minimum value being tracked by each distribution's histogram, `max` is the minimum value being tracked by each distribution's histogram, and `bkt` is each distribution's the number of values in each bucket |
|`Derived & subname(off_type index, const std::string &name)` | adds a name to the statistic at the given index                        |
|`Derived & subdesc(off_type index, const std::string &desc)` | adds a description to the statistic at the given index                 |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the distribution at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::VectorStandardDeviation`
Storing a vector of standard deviations where each element of the vector has function signatures similar to those of `Stats::StandardDeviation`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorStandardDeviation & init(size_type size)`             | initializes a vector of `size` standard deviations                     |
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                         |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index                  |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the standard deviation at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::VectorAverageDeviation`
Storing a vector of average deviations where each element of the vector has function signatures similar to those of `Stats::AverageDeviation`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorAverageDeviation & init(size_type size)`              | initializes a vector of `size` average deviations                      |
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                         |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index                  |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the average deviation at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::Formula`
Storing a statistic that is a result of a series of arithmetic operations on `Stats` objects.
Note that, in the following function, `Temp` could be any of `Stats` class holding statistics (including vector statistics), a formula, or a number (e.g.`int`, `double`, `1.2`).

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`const Formula &operator=(const Temp &r)`                    | assigns an uninitialized `Stats::Formula` to the given root            |
|`const Formula &operator=(const T &v)`                       | assigns the formula to a statistic or another formula or a number      |
|`const Formula &operator+=(Temp r)`                          | adds to the current formula a statistic or another formula or a number  |
|`const Formula &operator/=(Temp r)`                          | divides the current formula by a statistic or another formula or a number |
|`void result(VResult &vec) const`                            | assigns the evaluation of the formula to the given vector; if the formula does *not* have a vector component (none of the variables in the formula is a vector), then the vector size is 1 |
|`Result total() const`                                       | returns the evaluation of the `Stats::Formula` as a double; if the formula does have a vector component (one of the variables in the formula is a vector), then the vector is turned in to a scalar by setting it to the sum all elements in the vector |
|`size_type size() const`                                     | returns 1 if the root element is not a vector, returns the size of the vector otherwise |
|`bool zero()`                                                | returns `true` if all elements in `result()` are 0's, returns `false` otherwise|

An example of using `Stats::Formula`,
```C++
Stats::Scalar totalReadLatency;
Stats::Scalar numReads;
Stats::Formula averageReadLatency = totalReadLatency/numReads;
```

---

## Appendix. Migrating to the new style of tracking statistics

### A new style of tracking statistics
gem5 statistics have a flat structure that are not aware of the hierarchical structure of `SimObject`, which usually contains stat objects.
This causes the problem of different stats having the same name, and more importantly, it was not trivial to manipulating the structure of gem5 statistics.
Also, gem5 did not offer a way to group a collection of stat objects into different groups, which is important to maintain a large number of stat objects.

[A recent commit](https://gem5-review.googlesource.com/c/public/gem5/+/19368) introduces `Stats::Group`, a structure intended to keep all statistics belong to an object.
The new structure offers an explicit way to reflect the hierarchical nature of `SimObject`
`Stats::Group` also makes it more explicit and easier to maintain a large set of `Stats` objects that should be grouped into different collections as one can make several `Stats::Group`'s in a `SimObject` and merges them to the `SimObject`, which is also a `Stats::Group` that is aware of its children `Stats::Group`'s.

Generally, this is a step towards a more structured `Stats` format, which should facilitate the process of manipulating the overall structure of statistics in gem5, such as filtering out statistics and producing `Stats` to more standardized formats such as JSON and XML, which, in turns, have an enormous amount of supported libraries in a variety of programming languages.

### Migrating to the new style of tracking statistics

*Notes*: Migrating to the new style is highly encouraged; however, the legacy style of statistics (i.e. the one with a flat structure) is still supported.

This guide provides a broad look of how to migrate to the new style of gem5 statistics tracking, as well as points out some concrete examples showing how it is being done.

#### `ADD_STAT`
`ADD_STAT` is a macro defined as,
```C++
#define ADD_STAT(n, ...) n(this, # n, __VA_ARGS__)
```
This macro is intended to be used in `Stats::Group` constructors to initilize a `Stats` object.
In other words, `ADD_STAT` is an alias for caling `Stats` object constructors.
For example, `ADD_STAT(stat_name, stat_desc)` is the same as,
```
  stat_name.parent = the `Stats::Group` where stat_name is defined
  stat_name.name = "stat_name"
  stat_name.desc = "stat_desc"
```
This is applicable for most of `Stats` data types with an exception that for `Stats::Formula`, the macro `ADD_STAT` can handle an optional parameter specifying the formula.
For example, `ADD_STAT(ips, "Instructions per Second", n_instructions/sim_seconds)`.


An example use case of `ADD_STAT` (and we refer to this example as "**Example 1**" throughout this section).
This example is also served as a template of constructing a `Stats::Group` struct.
```C++
    protected:
        // Defining the a stat group
        struct StatGroup : public Stats::Group
        {
            StatGroup(Stats::Group *parent); // constructor
            Stats::Histogram histogram;
            Stats::Scalar scalar;
            Stats::Formula formula;
        } stats;

    // Defining the declared constructor
    StatGroup::StatGroup(Stats::Group *parent)
      : Stats::Group(parent),                           // initilizing the base class
        ADD_STAT(histogram, "A useful histogram"),
        scalar(this, "scalar", "A number"),             // this is the same as ADD_STAT(scalar, "A number")
        ADD_STAT(formula, "A formula", scalar1/scalar2)
    {
        histogram
          .init(num_bins);
        scalar
          .init(0)
          .flags(condition ? 1 : 0);
    }
```

#### Moving to the new style
Those are concrete examples of converting stats to the new style: [here](https://gem5-review.googlesource.com/c/public/gem5/+/19370), [here](https://gem5-review.googlesource.com/c/public/gem5/+/19371) and [here](https://gem5-review.googlesource.com/c/public/gem5/+/32794).

Moving stats to the new style involves:
  - Creating a struct `Stats::Group`, and moving all stats variables there. This struct's scope should be `protected`. The declaration of stat variables is usually in the header files.
  - Getting rid of `regStats()`, and moving the initialzation of stat variables to `Stats::Group` constructor as shown in **Example 1**.
  - In both header files and cpp files, all stats variables should be pre-appended by the newly created `Stats::Group` name as the stats are now under the `Stats::Group` struct.
  - Updating the class constructors to initialize `Stats::Group` variable. Usually, it's adding `stats(this)` to the constructors assuming the name of the variable is `stats`.

Some examples,
  - An example of `Stats::Group` declaration is [here](https://gem5.googlesource.com/public/gem5/+/refs/tags/v20.0.0.3/src/cpu/testers/traffic_gen/base.hh#194).
Note that all variables of type starting with `Stats::` have been moved to the struct.
  - An example of a `Stats::Group` constructor that utilizes `ADD_STAT` is [here](https://gem5.googlesource.com/public/gem5/+/refs/tags/v20.0.0.3/src/cpu/testers/traffic_gen/base.cc#332).
  - In the case where a stat variable requiring additional initializations other than `name` and `description`, you can follow [this example](https://gem5.googlesource.com/public/gem5/+/refs/tags/v20.0.0.3/src/mem/comm_monitor.cc#105).
