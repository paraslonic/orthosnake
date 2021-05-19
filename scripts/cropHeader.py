from Bio import SeqIO
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument('-input', type=str, default=None, help='input FASTA formated file')
parser.add_argument('-out', type=str, default=None, help='output FASTA formated file with header cropped to N symbols')
parser.add_argument('-n', type=int, default=None, help='maximum length of header')

args = parser.parse_args()

with open(args.out, 'w') as output:
    for seq_record in SeqIO.parse(args.input, "fasta"):
        header = seq_record.description
        seq_record.description=""
        new_header = (header[:(args.n-2)] + '..') if len(header) > args.n else header
        seq_record.id = new_header
        SeqIO.write(seq_record, output, "fasta")
    
    