---
layout: documentation
title: FAQ
doc: gem5art
parent: main
permalink: /documentation/gem5art/main/faq
---

# Frequently Asked Questions

**What is gem5art?**

gem5art (libraries for artifacts, reproducibility and testing) is a set of python modules to do experiments with gem5 in a reproducible and structured way.

**Do I need celery to run gem5 jobs using gem5art?**

Celery is not required to run gem5 jobs with gem5art.
You can use any other job scheduling tool or no tool at all.
In order to run your job without celery, simply call the run() method of your run object once it is created.
For example, assuming created run object (in a launch script) is called run, you can do the following:

```python
run.run()
```

**Is there a more user-friendly way to launch gem5 jobs?**

You can use python multiprocessing library based function calls (provided by gem5art) to launch multiple gem5 jobs in parallel.
Specifically, you can call the following function in your gem5art launch script:

```python
run_job_pool([a list containing all run objects to execute], num_parallel_jobs = [Number of parralel jobs])
```

**How to access/search the files/artifacts in the database?**

You can use the pymongo API functions to access the files in the database.
gem5art also provides methods that make it easy to access the entries in the database.
You can look at the different available methods [here](artifacts.html#searching-the-database).

**What if I want to re-run an experiment, using the same artifacts?**

As explained in the documentation, when a new run object is created in the launch script,
a hash is created out of the artifacts that this run is dependent on.
This hash is used to check if a the same run exists in the database.
One of the artifacts used to create the hash is runscript artifact (which basically is same as
experiments repository artifact, as gem5 configuration scripts are part of the base experiments
repository).
The easiest way to re-run an experiment is to update the name field of your launch script and commit the changes
in the launch script to the base experiments repository.
Make sure to use the new name field to query the results or runs in the database.

**How can I monitor the status of jobs launched using gem5art launch script?**

Celery does not explicitly show the status of the runs by default.
[flower](https://flower.readthedocs.io/en/latest/), a Python package, is a web-based tool for monitoring and administrating Celery.

To install the flower package,
```sh
pip install flower
```

If you are using celery to run your tasks, you can use celery monitoring tool called flower.
For this purpose, use the following command:

```sh
flower -A gem5art.tasks.celery --port=5555
```

You can access this server on your web browser using `http://localhost:5555`.

Celery also generates some log files in the directory where you are running celery from.
You can also look at those log files to know the status of your jobs.

**How to contribute to gem5art?**

gem5art is open-source.
If you want to add a new feature or fix a bug, you can create a PR on the gem5art github repo.
