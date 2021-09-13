import sys
import os
from Bio import SeqIO
import pandas as pd
# This script makes orthogroup fasta files
'''
It works like this:
    1. It reads a fiel with a lsit of required ogs and makes ogList
    2. Read orthogroups file as dataframe with two columns: og and gene. The gene column contains space separated gene names
    3. Detete from orthogroups frame all ogs that is not in ogList
    4. It reads a fasta file which contains sequences of all genes, creates a dictionary from it
    5. it itetate over rows of orthogroups frame, in every row it iterates over gene names, for all gene name it looks for its sequence in sequences dicionary. Then it white sequence to og fasta file
'''

orthologousGroupsFile = sys.argv[1] # a text with orthologs. The file format is 'orthogroup1 : gene1 gene 2 gene3', one orthogroup on one line
sequencesFile= sys.argv[2]; # fasta file with all genes sequences
ogListFile=sys.argv[3] # A fiel with names of required orthogroups. One og on one line
outputFolder=sys.argv[4] # output folder :)

import sys
import os
from Bio import SeqIO
import pandas as pd
# This script makes orthogroup fasta files
'''
It works like this:
    1. It reads a file with a sit of required ogs and makes ogList
    2. Read orthogroups file as dataframe with two columns: og and gene. The gene column contains space separated gene names
    3. Detete from orthogroups frame all ogs that is not in ogList
    4. It reads a fasta file which contains sequences of all genes, creates a dictionary from it
    5. it itetate over rows of orthogroups frame, in every row it iterates over gene names, for all gene name it looks for its sequence in sequences dicionary. Then it white sequence to og fasta file
'''

try:
    os.makedirs(outputFolder)
except OSError:
    print ("Creation of the directory %s failed" % outputFolder)
else:
    print ("Successfully created the directory %s" % outputFolder)

ogList = []

# create list of the ogs
# it just read the ogListFile as csv dataframe with only one column, and values of this column are trasformed to a list
ogList = list(pd.read_csv(ogListFile, header = None)[0])

# read orthogroups.txt as dataframe, which has two columns: ogs and genes of ogs
orthoFile = pd.read_table(orthologousGroupsFile, header = None, sep = ':').set_axis(['og', 'genes'], axis = 1)
orthoFile.genes = orthoFile.genes.apply(lambda x: x.strip()) # delete technical characters and spaces
orthoFile = orthoFile[orthoFile.og.isin(ogList)] # delete all orthogroups that are not in ogList

# make a dictionary with names of genes as keys and its sequences as values
seq_dict = {}
for seq_record in SeqIO.parse(sequencesFile, "fasta"):
    seq_dict['|'.join(seq_record.id.split('|')[0:2])] = str(seq_record.seq) # orthofinder renames genes that contain '()' or ',', because of this the script works with names truncated to format 'genone|gene id' 
# make og fasta files
for index, row in orthoFile.iterrows(): # iter over ogs
    og = row[0]
    genes = row[1]
    with open((outputFolder+og+ '.fasta'), 'w') as handle: # open og fasta file
        for gene in genes.split(' '): # iter over genes of the og
            handle.write(('>'+gene+'\n'))
            handle.write((seq_dict.pop('|'.join(gene.split('|')[0:2]))) + '\n') # look for sequence of the gene and write it