# receive a fodler with fasta_file and a fodler for mapfiles
import sys
import os
from random import shuffle
from Bio.SeqIO import parse
fasta_file = sys.argv[1]
map_file = sys.argv[2]
nucs = parse(fasta_file, format='fasta')
with open(map_file, "w") as handle:
    for nuc in nucs:
        full_name = nuc.id
        full_nameSp = full_name.split("|")[0]
        handle.write((full_name + " " + full_nameSp + "\n"))
