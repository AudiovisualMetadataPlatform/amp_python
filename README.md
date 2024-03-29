# AMP MGM Runtime

Provide a consistent set of runtime libraries and utilities to
AMP MGMs when run under galaxy.

The runtime consists of two parts:
* A apptainer container set up as a python 3.10 interpreter
* A python library that provides functionality useful for MGMs

## The python container
The python container is based on Fedora 36 

You can browse around the container by running:

apptainer exec app_python.sif /bin/bash

Note:  The current directory, home directory, /tmp, and a few
other directories are mounted from the host system, but
/bin, /usr/bin, and others come from the container.

Note: apptainer is not provided by this container.

## Building
Check out this repository into `$AMP_ROOT/src_repos` and then within the amp_bootstrap, run `./amp_devel build amp_python`

To install, config, run AMPPD, as well as contribute to the AMP project, please refer to the instructions on [AMP Bootstrap](https://github.com/AudiovisualMetadataPlatform/amp_bootstrap)
