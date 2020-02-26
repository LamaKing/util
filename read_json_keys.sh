#!/bin/bash

# Read selected keys from a json file.
# NOTE: nested json not supported.
# FIXME: can't get it to automatically allocate variables for keys.
# Silva 13-09-19 (created 13-09-19)

#-----------------------------------------------------------
# Read Dictionary Function
#-----------------------------------------------------------
# Read a python-like dictionary file: key="value is arbitrary string"
function read_json_keys {
    # First arg is file name, the rest are keys.
    c_file=$1
    keys=${@:2}
    for i in ${keys[@]}
    do
	# Look for they and separate it (before =) from value (all after =).
	#field="$(sed -En "/^$i=/p" $c_file | cut -d "=" -f 2-)"
    # Read the file, remove the json {} formats, transfonr , to newline so bash can read it easier.
    # Look for the key you want and save it. Trim whitespaces from variable
    field="$(cat $c_file | tr -d "{}" | tr "," "\n" | sed -En "/$i*:*/p" | cut -d ":" -f 2- | sed "s:^[[:space:]]:: ; s:[[:space:]]$::")"
    if [ ! "$field" ] ; then
	    echo "Missing param $i in config file $c_file"
	    exit 1
	fi
	# Create bash variable with key and assign field to it.
	eval "$i=\"$field\""
    done
}
