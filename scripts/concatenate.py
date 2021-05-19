"Параметры на вход работают несколько криво, надо допилить, пример активации: concatenate.py input_folder/*fasta output_folder/output.fasta"
import glob
import os
#from Bio import SeqIO
from Bio.SeqIO import parse
from sys import argv

file_input = argv[1:-1] 
file_output= argv[-1];
dict = {}
for file in file_input:
    with open(file, "r") as fastaFile:
        for record in parse(fastaFile, "fasta"):
            None
            id =(record.id).split("|")[0]
            seq = record.seq
            if id not in dict.keys():
                dict[id]=seq
            else:
                dict[id]+=seq
with open(file_output, "w") as handle:
    for i in dict.keys():
        handle.write(">"+i+"\n")
        handle.write(str(dict[i])+"\n")
