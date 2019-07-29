snakemake script to infere orthogroups with fasta-formated genomes as the input. Genomes are annotated with prokka first. Then orthofinder is run.
Requires [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) and [conda3](https://conda.io/en/latest/) to be installed.\
Please place fasta formated genomes (with .fna extension) in the fna folder.\
Run with `snakemake --use-conda`

If genome files have extension other than .fna please rename them, i.e. with following command:
`for i in fna/*.fasta; do mv $i fna/$(basename $i .fasta).fna; done`

fna folder contains three example sequences of *E. coli* plasmids for test run of the script. 
