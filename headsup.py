#!/usr/bin/env python

# landscape-sysinfo-mini.py -- a trivial re-implementation of the
# sysinfo printout shown on debian at boot time. No twisted, no reactor, just /proc.
#
# Loosly based on https://github.com/jnweiger/landscape-sysinfo-mini which in turn was
# inspired by ubuntu 14.10 /etc/update-motd.d/50-landscape-sysinfo

from __future__ import division

import os
import re
import subprocess
import time


def main():
    # update-motd.d scripts must start with printing a single blank line
    print
    load_average = get_system_load_average()
    processes = get_number_of_running_processes()
    defaultdev = get_default_net_device()
    root_usage, root_size_in_gb = get_root_fs_stats()
    ipaddr = get_device_address(defaultdev)
    num_users = get_number_of_logged_in_users()
    memory_usage, swap_usage = get_memory_stats()

    # For percentages, direct percentage formatting with '{:.2%}'.format(val)
    # could also have been used, but was found to be significantly slower than the
    # equivalent %-style formatting.
    print("  System information as of %s\n" % time.asctime())
    print("  System load:  %.1f%%              Processes:        %d" % (load_average*100, processes))
    print("  Usage of /:   %.1f%% of %.2fGB   Users logged in:  %d" % (root_usage*100, root_size_in_gb, num_users))
    print("  Memory usage: %.1f%%              IP address for %s: %s" % (memory_usage*100, defaultdev, ipaddr))
    print("  Swap usage:   %s" % (".1f%%" % (swap_usage*100) if swap_usage is not None else '---'))
