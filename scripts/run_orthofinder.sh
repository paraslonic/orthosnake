orthofinder=$1
threads=$2
orthofinder -t $threads -a $threads -og -f faa
mkdir -p tmp
find faa -name 'Orthogroups.txt' -exec cp {} tmp \; 
find faa -name 'Orthogroups.csv' -exec cp {} tmp \; 
perl scripts/namedGroups2table.pl tmp/Orthogroups.txt
mv ortho_table_names.txt ortho_table.txt tmp
