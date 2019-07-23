#!/bin/sh
# Fetch the latest Samuellab source code using Jonathan Epstein's read-only Github token.
#
# Please do not redistribute this script outside of HHMI Janelia!

curl -H "Authorization: token b58f801e21e2c2f4b424ebf18a274158d22045ee" -L -o Matlab-Track-Analysis.tar.gz \
    https://api.github.com/repos/samuellab/Matlab-Track-Analysis/tarball

curl -H "Authorization: token b58f801e21e2c2f4b424ebf18a274158d22045ee" -L -o Janelia-Software.tar.gz \
    https://api.github.com/repos/samuellab/Janelia-Software/tarball

# unpack these archives and rename the corresponding directories to Matlab-Track-Analysis
#       and Janelia-Software

zcat Matlab-Track-Analysis.tar.gz | tar xf -
mv samuellab-Matlab-Track-Analysis* Matlab-Track-Analysis

zcat Janelia-Software.tar.gz | tar xf -
mv samuellab-Janelia-Software* Janelia-Software
