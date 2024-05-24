#!/bin/bash


FILE_SIZE_LIMIT=50


function check_file_size {
    size=$(du -m $1 | awk '{print $1}')
    if (($size > $FILE_SIZE_LIMIT)); then
       echo "Size of file $1 is greater than ${FILE_SIZE_LIMIT}M"
       exit 1
    fi
}


function traverse_and_validate {
    for object in $1/*
        do
            if [ -d $object ]; then
                # echo $object is a directory
		        if [[ "$object" =~ ^$1/venv.*$ ]]; then
		            # echo subdir $object is virtualenv
		            :
		        else
                    # echo Entering to subdir $object
                    traverse_and_validate $object
		        fi
		        # echo Leaving subdir $object
            else
                # echo $object is a file
		        check_file_size $object
            fi
        done
}

traverse_and_validate .
