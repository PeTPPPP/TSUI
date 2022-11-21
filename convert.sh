pdfcrop "$1" "$1-temp"
pdftops -f 1 -l 1 -eps "$1-temp" "${1:0:(-4)}.eps"
rm  "$1-temp"

${stringZ:(-4)}  