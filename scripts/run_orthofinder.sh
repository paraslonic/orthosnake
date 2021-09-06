threads=$1
orthofinder -t $threads -a $threads -og -f tmp/genome_fasta_aa
mkdir -p tmp
find tmp/genome_fasta_aa -name 'Orthogroups.txt' -exec cp {} Results \; 
find tmp/genome_fasta_aa -name 'Orthogroup_Sequences' -exec cp -r {} tmp/og_fasta_aa \;
