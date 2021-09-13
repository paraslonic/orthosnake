from Bio.SeqIO import parse
import os
import sys

nuc_file = sys.argv[1]
prot_file = sys.argv[2]
out_file = sys.argv[3]
seq_dict = {}
nucs = parse(nuc_file, format='fasta') # nucs - current nucleotide fasta file
for rec in nucs: # 
    prots = parse(prot_file, format='fasta')

    for prot_rec in prots:

        if rec.description in prot_rec.description:
            nuc_seq = ''
            S = 0
            N = 0
            for i in range(len(prot_rec.seq)):
                if prot_rec.seq[i] != '-':
                    nuc_seq += str(rec.seq[(i-S)*3: (i-S)*3 + 3])
                    continue
                else:
                    S += 1
                    nuc_seq += '-'
                    nuc_seq += '-'
                    nuc_seq += '-'
                    continue
            seq_dict[rec.description] = str(nuc_seq)
            break

with open(out_file, 'w') as fout:
    for name in seq_dict:
        fout.write('>' + name)
        fout.write('\n')
        fout.write(seq_dict[name])
        fout.write('\n')
            

