# Добавить создание fasta с нуклеотидами и аминокислотами с ортогруппами из orthogrops.txt в папку tmp.
# Выравнять аминкоислоты
# По аминокислоатм выравнять нуклеотиды
# Генеракс
#GENOMES, = glob_wildcards("tmp/og_fasta_aa/{og}.fa")
#rule all: 
#    input: expand("tmp/og_aligned_aa/{og}.fasta", og=GENOMES)

import pandas as pd
ogs = pd.read_table('Results/Orthogroups.txt', sep = ':', header=None)
ogs = list(ogs[0])

