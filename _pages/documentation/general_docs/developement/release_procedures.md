---
layout: documentation
title: "Release Procedures"
doc: gem5 documentation
parent: development
permalink: /documentation/general_docs/development/release_procedures/
---

Information on when releases are carried out, how the community is notified, versioning information, and how to contribute to a release can be found in our [CONTRIBUTING.md document](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/CONTRIBUTING.md#releases).
The purpose of this document is to outline specific procedures carried out during a release.

## gem5 repository

The [gem5 git repository](https://gem5.googlesource.com/public/gem5/) has two branches, [stable](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable) and [develop](https://gem5.googlesource.com/public/gem5/+/refs/heads/develop).
The HEAD of the stable branch is the latest official release of gem5 and will be tagged as such.
Users are not permitted to submit patches to the stable branch, and instead submit patches to the develop branch.
At least two weeks prior to a release a staging branch is created from the develop branch.
This staging branch is rigorously tested and only bug fixes or inconsequential changes (format fixes, typo fixes, etc.) are permitted to be be submitted to this branch.

The staging branch is updated with the following changes:

* The `-werror` is removed.
This ensures that gem5 compiles on newer compilers as new/stricter compiler warnings are incorporated.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/43425>.
* The [Doxygen "Project Number" field](https://gem5.googlesource.com/public/gem5/+/refs/tags/v21.0.1.0/src/Doxyfile#34) is updated to the version ID.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/47079>.
* The [`src/base/version.cc`](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/base/version.cc) file is updated to state the version ID.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/47079>.
* The [`ext/testlib/configuration.py`](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/ext/testlib/configuration.py)  file's `default.resource_url` field is updated to point towards the correct Google Cloud release bucket (see [the Cloud Bucket release procedures](#gem5-resources-google-cloud-bucket)).
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/44725>.

When the staging branch is confirmed to be in a satisfactory state, it will be merged into both develop and stable.
There is then two additional actions:

1. The above changes to the staging branch are reverted on the develop branch.
2. The stable branch is tagged with the latest release version id at its HEAD.
    * For example, `git tag -a v21.1.0.0 -m "gem5 version 21.1.0.0" && git push --tags`

The [RELEASE-NOTES.md](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/RELEASE-NOTES.md) should be updated to notify the community of the major changes in this release.
This can be done on the develop branch prior to the creation of the staging branch, or on the staging branch.
It has been customary to create a blog post on <http://www.gem5.org> outlining the release.
While appreciated, it is not mandatory.

**Important notes:**
* You must a member of the "Project Owners" or "google/gem5-admins@googlegroups.com" Gerrit permission groups to push to the stable branch.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing to the gem5 stable branch.

## gem5 resources repository

The [gem5 resources git repository](https://gem5.googlesource.com/public/gem5-resources) has two branches, [stable](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable) and [develop](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/develop).
The HEAD of the stable branch contains the source for resources with known compatibility to the most recently release of gem5.
E.g., if the current release of gem5 is v22.3, the head of gem5 resources repository will contain the source for resources with known compatibility with v22.3.
The develop branch contains sources compatible with the develop branch of the gem5 repository.
Unlike the gem5 repo, changes to the gem5 resources repo may be submitted to the stable branch permitting the changes are compatible with the latest release of gem5.

As with the gem5 repository, a staging branch is created at least two weeks prior to a release.
The purpose of this staging branch is identical to that of the main gem5 repository, and it is merged into both the stable and develop branches upon a gem5 release.
Prior to this the following changes should be applied to the staging branch:

* A new Google Cloud Bucket directory should be created for that version (see the [the Cloud Bucket release procedures](#gem5-resources-google-cloud-bucket)), and all the resources from the staging branch must match that found within that Google Cloud Bucket directory (i.e., the compiled resources within the bucket are built from the sources in the staging branch).
* URL download links in the resources repo should be updated to point towards the correct Google Cloud Bucket directory.

When merged into the develop branch, the URL download links should reverted back to `http://dist.gem5.org/dist/develop`.

Immediately prior to merging, the stable branch is tagged with the previous release version ID.
For example, if the staging branch is for `v22.2,` and the content on the stable branch is for `v22.1`, the stable branch will be tagged as `v22.1` immediately prior to the merge.
This is because we want users to be able to revert the gem5 resources to get sources compatible with previous gem5 releases.
Therefore, if a user wished to get the resources sources compatible with the the v20.1 release, they'd checkout the revision tagged as `v20.1` on the stable branch.

### gem5 resources Google Cloud Bucket

The built gem5 resources are found within the gem5 Google Cloud Bucket.

The [gem5 resources git repository](#gem5-resources-repository) contains sources of the gem5 resources, these are then compiled and stored in the Google Cloud Bucket.
The gem5 resources repo [README.md](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md) contains links to download the built resources from the Google Cloud Bucket.

The Google Cloud Bucket, like the gem5 resources repository, is versioned.
Each resource is stored under `http://dist.gem5.org/dist/{major version}`.
E.g., the PARSEC Benchmark image, for version 20.1, is stored at <http://dist.gem5.org/dist/v20-1/images/x86/ubuntu-18-04/parsec.img.gz>, while the image for version 21.0 is stored at <http://dist.gem5.org/dist/v21-0/images/x86/ubuntu-18-04/parsec.img.gz> (note the `.` substitution with `-` for the version in the URL).
The build for the develop branch is found under <http://dist.gem5.org/dist/develop>.

As the gem5 resources staging branch is from develop, the easiest way to create a copy of the develop bucket directory:

```
gsutil -m cp -r gs://dist.gem5.org/dist/develop gsutil -m cp -r gs://dist.gem5.org/dist/{major version}
```

The develop bucket _should_ be in-sync with the changes on develop.
Though this is worth checking.
Naturally, any changes on the staging branch must be reflected in the Cloud Bucket accordingly.

**Important notes:**
* Due to legacy reason <http://dist.gem5.org/dist/current> is used to store legacy resources related to v19 of gem5.
* Special permissions are needed to push to the Google Cloud Bucket.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing resources to the bucket.

## The docker images

Currently hosted in [`util/dockerfiles`](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/util/dockerfiles/) in the gem5 repository, we have a series of Dockerfiles which can be built to produce environments in which gem5 can be built and run.
These images are mostly used for testing purposes.
The [`ubuntu-20.04_all-dependencies`](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/util/dockerfiles/ubuntu-20.04_all-dependencies/) Dockerfile is the one most suitable for users who wish to build and execute gem5 in a supported environment.

We provide pre-built Docker images, hosted at <gcr.io/gem5-test>.
All the Dockerfiles found in `util/dockerfiles` have been built and stored there.
For instance, `ubuntu-20.04_all-dependencies` can be found at <gcr.io/gem5-test/ubuntu-20.04_all-dependencies> (and can thereby be obtained with `docker pull cr.io/gem5-test/ubuntu-20.04_all-dependencies`).

The Docker images are continually built from the Dockerfiles found on the develop branch.
Therefore the docker image with the `latest` tag is that in-sync with the Dockerfiles found on the gem5 repo's develop branch.
Upon a release of the latest version of gem5, when the staging branches are merged into develop, the built images hosted at <grc.io/gem5-test> will be tagged with the gem5 version number.
So, upon the release of `v23.2`, the images will be tagged with `v23-2`
The purpose of this is so users of an older versions of gem5, may obtain images compatible with their release.
I.e., a user of gem5 `v21.0` may obtain the `v21.0` version of the `ubuntu-20.04_all-dependencies` with `docker pull cr.io/gem5-test/ubuntu-20.04_all-dependencies:v21-0`.

**Important notes:**
* If changes to the Dockerfile are done on the staging branch, then these changes will need to be pushed to <gcr.io/gem5-test> manually.
* Special permissions are needed to push to the <gcr.io/gem5-test>.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing images.
* It is a future goal to of ours to move [the Dockerfiles from `util/dockerfiles` to gem5-resources](https://gem5.atlassian.net/browse/GEM5-1044).

## gem5 website repository

The [gem5 website git repository](https://gem5.googlesource.com/public/gem5-website/) has two branches, [stable](https://gem5.googlesource.com/public/gem5-website/+/refs/heads/stable) and [develop](https://gem5.googlesource.com/public/gem5-website/+/refs/heads/develop).
The stable branch is what is built and viewable at <http://www.gem5.org>, and is up-to-date with the current gem5 release.
E.g., if the current release of gem5, on its stable branch, is `v20.1`, the documentation on the stable branch will related to `v20.1`.
The develop branch contains the state of the website for the upcoming gem5 release.
E.g., it contains the changes needed to apply to the website when the new version of gem5 is released.

As the stable branch may be updated at any time (as long as those updates relate to the current release), stable is merged periodically into develop.
As with the gem5 resources, and the main gem5 repository, a staging branch is created from the develop branch at least two weeks prior to a gem5 release.

The staging branch needs updated so that the documentation is up-to-date with the upcoming release.
Of particular note, references to gem5 resources, hosted on the Google Cloud bucket should be updated.
For example, links to, say <http://dist.gem5.org/dist/v21-0/images/x86/ubuntu-18-04/parsec.img.gz>, would need to be updated to <http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/parsec.img.gz> when transitioning from `v21-0` to `v21-1`.

Upon a new major gem5 release, the develop branch is merged into stable.
The website repo is tagged with the preceding version prior to merging the staging branch into stable.
This is identical to the gem5 resources repository.
For example, if the current release is v21.1.0.4 and the next release is v21.2.0.0, immediately prior to the release of v21.2.0.0 the stable branch will be tagged as v21.1.0.4 then the develop branch merged into stable.
This ensures that a user may revert the website back to its state as of a previous release, if needed.

## gem5 Doxygen

The [gem5 Doxygen website](http://doxygen.gem5.org) is created by the [Doxygen documentation generator](https://www.doxygen.nl/index.html).
It can be created in gem5 repo as follows:

```
cd src
doxygen
```

The html will be output to `src/doxygen/html`.

The gem5 Doxygen website is hosted as a static webpage in a Google Cloud Bucket.
The directory structure is as follows:

```
doxygen.gem5.org/
    - develop/              # Contains the Doxygen for the gem5 develop branch.
        - index.html
        ...
    - release/              # An archive of the Doxygen for every gem5 release.
        - current/          # Doxygen for the current gem5 release.
            - index.html
            ...
        - v21-0-1-0/
            - index.html
            ...
        - v21-0-0-0/
            - index.html
            ...
        - v20-1-0-5/
            - index.html
            ...
        ...
    - index.html           # Redirects to release/current/index.html.
```

Therefore, the Doxygen for the latest release can be obtained at <http://doxygen.gem5.org/>, for the develop branch at <http://doxygen.gem5.org/develop>, and for past releases at <http://doxygen.gem5.org/release/{version}> (e.g., <http://doxygen.gem5.org/release/v20-1-0-5>).

After a gem5 release the following code is run on the gem5 repository stable branch

```
cd src
doxygen

gsutil -m rm gs://doxygen.gem5.org/release/current/*
gsutil -m cp -r doxygen/html/* gs://doxygen.gem5.org/release/current/
gsutil -m cp -r gs://doxygen.gem5.org/release/current gs://doxygen.gem5.org/release/{version id}
```

The final step is to add a link to this gem5 Doxygen version on the website, via the [`_data/documentation.yml` file](https://gem5.googlesource.com/public/gem5-website/+/refs/heads/stable/_data/documentation.yml).
For example: <https://gem5-review.googlesource.com/c/public/gem5-website/+/43385>.


**Important Notes:**
* The gem5 develop branch Doxygen website is updated daily via an automated build process.
The footer on the Doxygen website will state when the page was generated.
* Special permissions are needed to push to the Google Cloud Bucket.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing to the Google Cloud Bucket.

## Minor and Hotfix releases

The previous sections have focus on major gem5 releases.
Minor and hotfix releases of gem5 should never change any API or features in a major way.
As such, for minor and hotfix releases of gem5 we only carry out the release procedures for the [gem5 code repository](#gem5-repository) and the [gem5 Doxygen website](#gem5-doxygen).
The latter may be unnecessary depending on the change/changes, but this is a low cost endeavor.