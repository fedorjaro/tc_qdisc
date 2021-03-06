#!/bin/bash

set -euo pipefail

if [ -n "${DEBUG:-}" ] ; then
    set -x
fi

if [ ! -d "${1:-}" -o ! -d "${2:-}" ] ; then
    exit 0
fi

# we need absolute path for $2
absmoddir=$( readlink -f "$2" )

# clean up old links to module_utils
for item in "$1"/* ; do
    if lnitem=$( readlink "$item" ) && test -n "$lnitem" ; then
        case "$lnitem" in
            *"${2}"*) rm -f "$item" ;;
        esac
    fi
done

# add new links to module_utils
for item in "$absmoddir"/* ; do
    case "$item" in
        *__pycache__) continue;;
        *.pyc) continue;;
    esac
    bnitem=$( basename "$item" )
    ln -s "$item" "$1/$bnitem"
done
