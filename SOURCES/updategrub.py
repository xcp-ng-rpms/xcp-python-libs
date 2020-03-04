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

import sys, getopt, os
from xcp import bootloader

def main(argv):
    is_default = False
    grubFile = str(grubPath())
    try:
        opts, args = getopt.getopt(argv,'ad:rd:',["add=","remove=","default"])
    except getopt.GetoptError:
	print "Help: Use [--default/-d] --add/-a alt-version or --remove/-r alt-version"
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-d', '--default'):
	    is_default = True
    for opt, arg in opts:
        if opt in ('-a', '--add'):
            add_kernel(arg, is_default, grubFile)
        elif opt in ('-r', '--remove'):
            remove_kernel(arg, grubFile)

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
# Params : is_default is to set the new kernel as default to boot
# Params : grubFile is the file path to write grub configuration
# Description : The function is used to add new entry by copying "XCP-ng" entry
# into "XCP-ng alt" such that the alt kernel is selected.
#

def add_kernel(arg, is_default, grubFile):
    b = bootloader.Bootloader("grub2", grubFile)
    b = b.loadExisting()
    ALT = arg
    item = 'xe'

# If ALT is already present, mark it for default
    for key, item in b.menu.items():
        if ALT in b.menu.get(key).kernel:
	    if is_default == True:
                b.default = key
		break

# If ALT is not present
    if "label" not in b.default: 
	new_entry = bootloader.MenuEntry(
        b.menu.get(key).hypervisor, 
	b.menu.get(key).hypervisor_args, 
	"/boot/vmlinuz-" + ALT + "-xen", 
	b.menu.get(key).kernel_args, 
	"/boot/initrd-" + ALT + "-xen.img", 
	b.menu.get(key).title + " kernel-alt " + ALT
	)
	b.append("alt", new_entry)
	key = "alt"

    if is_default == True:
	b.default = key
    else:
	b.default = 'xe'
    b.writeGrub2(grubFile)
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
    item = 'xe'
    for key, item in b.menu.items():
        if ALT in b.menu.get(key).kernel:
		b.remove(key)

    b.default = 'xe'
    b.writeGrub2(grubFile)
    return True

if __name__ == "__main__":
   main(sys.argv[1:])
