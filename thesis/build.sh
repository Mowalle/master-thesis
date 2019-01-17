#!/usr/bin/env bash

if [ -z $1 ]; then
    echo "Must pass the .tex's filename as first argument!"
    exit 1
fi

filename=$(basename $1 .tex)

if [ "$2" == "-build" ] || [ "$3" == "-build" ]; then 
    latexmk -outdir=build -pdf -synctex=1 "$filename.tex"
fi

if [ "$2" == "-view" ] || [ "$3" == "-view" ]; then 
    find . -name "$filename.pdf" -exec xdg-open {} \; -quit
fi


