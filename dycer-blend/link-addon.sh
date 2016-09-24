#!/bin/bash

#addons_dir=~/.config/blender/2.77/scripts/addons
addons_dir=/Applications/Blender\ 2.77a.app/Contents/Resources/2.77/scripts/addons_contrib
addon_dir=$addons_dir/dycer

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# create the Python script directory
if [ ! -e "$addons_dir" ]
then
    echo "Addons directory does not exist, so creating $addons_dir"
    mkdir -p "$addons_dir"
fi

# link the Python script directory
if [ -e "$addon_dir" ]
then
    echo "Addon already linked - exiting"
    exit 0
else
    echo "Linking ${script_dir} to ${addon_dir}"
    ln -s "${script_dir}" "${addon_dir}"
fi
