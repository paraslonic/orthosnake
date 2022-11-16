from Bio import SeqIO
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument('-gb', type=str, default=None, help='GenBank file')

args = parser.parse_args()


file = args.gb
gbs = [seq for seq in SeqIO.parse(open(file), 'genbank')]
name = os.path.basename(file)
name = os.path.splitext(name)[0]
id_ = 1
for gb in gbs:
    contig = gb.name
    feats = [feat for feat in gb.features if feat.type=='CDS' and ('translation' in feat.qualifiers.keys())]
    for feat in feats:
        print('>' + name + '|' +
                str(id_) + '|' +
                feat.qualifiers['product'][0].replace(' ', '_') + '|' +
                contig + '|' + str(feat.location.start) + '|' +
                str(feat.location.end))

        print(feat.qualifiers['translation'][0])
        id_ += 1
