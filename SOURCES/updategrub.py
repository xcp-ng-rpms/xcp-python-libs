#!/usr/bin/env python

# Copyright (C) 2020 - Vates
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, argparse
from xcp import bootloader

def main(argv):
    grubFile = str(grubPath())
    try:
        parser = argparse.ArgumentParser(description='UpdateGrub script to \
                                                      handle grub kernel-alt entries')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--add', '-a')
        group.add_argument('--remove', '-r')
        group.add_argument('--set_default', '-d')
        results = parser.parse_args()
    except Exception as e:
        print >> sys.stderr, e
        sys.exit(1)
    if results.add:
        if not add_kernel(results.add, grubFile):
            print >> sys.stderr, "alt-kernel " + results.add + " is already added."
            sys.exit(2)
    elif results.remove: 
        if not remove_kernel(results.remove, grubFile):
            print >> sys.stderr, "No grub entry found for kernel " + results.remove
            sys.exit(3)
    elif results.set_default:
        if not set_kernel(results.set_default, grubFile):
            print >> sys.stderr, "No grub entry found for kernel " + results.set_default
            sys.exit(4)

#
# Function Name : grubPath
# Params : root = '/'
# Description : The function is used to find the grub file path.
#

def grubPath(root = '/'):
    if os.path.exists(os.path.join(root, "boot/efi/EFI/xenserver/grub.cfg")):
        return (os.path.join(root, "boot/efi/EFI/xenserver/grub.cfg"))
    elif os.path.exists(os.path.join(root, "boot/grub/grub.cfg")):
        return (os.path.join(root, "boot/grub/grub.cfg"))
    elif os.path.exists(os.path.join(root, "boot/grub2/grub.cfg")):
        return (os.path.join(root, "boot/grub2/grub.cfg"))
    elif os.path.exists(os.path.join(root, "boot/extlinux.conf")):
        return cls.readExtLinux(os.path.join(root, "boot/extlinux.conf"))
    elif os.path.exists(os.path.join(root, "boot/grub/menu.lst")):
        return (os.path.join(root, "boot/grub/menu.lst"))
    else:
        raise RuntimeError, "No existing bootloader configuration found"

#
# Function Name : add_kernel
# Params : arg is "alt" kernel version e.g. 4.19.102
# Params : grubFile is the file path to write grub configuration
# Description : The function is used to add new entry by copying "XCP-ng" entry
# into "XCP-ng alt" such that the alt kernel can be selected.
#

def add_kernel(arg, grubFile):
    b = bootloader.Bootloader("grub2", grubFile)
    b = b.loadExisting()
    ALT = arg

    # If ALT is already present, return
    for key, item in b.menu.items():
        if ALT in b.menu.get(key).kernel:
            return False

    # If ALT is not present, use default kernel as template
    key = 'xe'
    new_entry = bootloader.MenuEntry(
    b.menu.get(key).hypervisor, 
    b.menu.get(key).hypervisor_args, 
    "/boot/vmlinuz-" + ALT + "-xen", 
    b.menu.get(key).kernel_args, 
    "/boot/initrd-" + ALT + "-xen.img", 
    b.menu.get(key).title + " kernel-alt " + ALT,
    root = b.menu.get(key).root
    )
    b.append("alt", new_entry)
    b.writeGrub2(grubFile)
    print "Adding kernel-alt " + arg + " as grub entry #" + str(len(b.menu)-1)
    return True

#
# Function Name : remove_kernel
# Params : arg is "alt" kernel version e.g. 4.19.102
# Params : grubFile is the file path to write grub configuration
# Description : The function is used to remove alt kernel entry
# and set "XCP-ng" as next default.
#

def remove_kernel(arg, grubFile):
    b = bootloader.Bootloader("grub2", grubFile)
    b = b.loadExisting()
    ALT = arg
    for key, item in b.menu.items():
        if ALT in b.menu.get(key).kernel:
            b.remove(key)
            b.default = 'xe'
            b.writeGrub2(grubFile)
            print "Removing kernel-alt " + arg + " from grub entries and " \
                  + "setting back main kernel as default grub entry"
            return True
    return False

#
# Function Name : set_kernel
# Params : arg is "alt" kernel version e.g. 4.19.102
# Params : grubFile is the file path to write grub configuration
# Description : The function is used to set alt kernel entry as next default.
#

def set_kernel(arg, grubFile):
    b = bootloader.Bootloader("grub2", grubFile)
    b = b.loadExisting()
    ALT = arg
    for key, item in b.menu.items():
        if ALT in b.menu.get(key).kernel:
            b.default = key
            b.writeGrub2(grubFile)
            print "Setting kernel-alt " + arg + " as default grub entry"
            return True

    return False

if __name__ == "__main__":
   main(sys.argv[1:])
