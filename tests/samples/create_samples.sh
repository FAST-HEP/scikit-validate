#!/usr/bin/env bash
python generate_samples.py

root -qbx histograms.cpp

root -qbx objects.cpp

root -qbx root_other.cpp
