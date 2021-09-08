import sys
import os
from Bio import SeqIO
import pandas as pd

orthologousGroupsFile = sys.argv[1] # файл с ортогруппами (txt)
sequencesFile= sys.argv[2]; # мультифаста со всеми последовательностями генов
ogListFile=sys.argv[3] # файл с именами огешек, которые нужно превратить в фасты
outputFolder=sys.argv[4] # папка куда будут записываться фасты на каждую отдельную ог-ку

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

# read orthogroups.txt as dataframe, which has twho columns: ogs and genes of ogs
orthoFile = pd.read_table(orthologousGroupsFile, header = None, sep = ':').set_axis(['og', 'genes'], axis = 1)
orthoFile.genes = orthoFile.genes.apply(lambda x: x.strip()) # delete technical characters and spaces
orthoFile = orthoFile[orthoFile.og.isin(ogList)] # delete all orthogroups that are not in ogList

# make a dictionary with names of genes as keys and its sequences as values
seq_dict = {}
for seq_record in SeqIO.parse(sequencesFile, "fasta"):
    seq_dict[seq_record.id] = str(seq_record.seq)
    
for index, row in orthoFile.iterrows():
    og = row[0]
    genes = row[1]
    with open((outputFolder+og+ '.fasta'), 'w') as handle:
        for gene in genes.split(' '):
            handle.write(('>'+gene+'\n'))
            handle.write((seq_dict.pop(gene) + '\n'))         