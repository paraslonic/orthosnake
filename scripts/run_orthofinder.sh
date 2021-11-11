threads=$1
orthofinder -t $threads -a $threads -og -f faa 
mkdir -p tmp
find faa -name 'Orthogroups.txt' -exec cp {} Results \; 
find faa -name 'Orthogroups_SingleCopyOrthologues.txt' -exec cp {} Results \;
