 mkdir faa; for f in gbk/*.gbff; do name=$(basename $f .gbff); python scripts/GBfaa.py -gb $f > faa/$name.fasta; done
