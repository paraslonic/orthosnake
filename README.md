snakemake script to infere orthogroups with fasta-formated genomes as the input. Genomes are annotated with prokka first. Then orthofinder is run.
Requires [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) and [conda3](https://conda.io/en/latest/) to be installed.\
Please place fasta formated genomes (with .fna extension) in the fna folder.\
Run with `snakemake --use-conda`

If genome files have extension other than .fna please rename them, i.e. with following command:
`for i in fna/*.fasta; do mv $i fna/$(basename $i .fasta).fna; done`

test_fna folder contains three example sequences of *E. coli* plasmids, which may be used for testing the pipeline. 

### Algorightm

* Fasta formated files are modified if neccessary to be consisten with prokka annotation tool.  
  * If header contains symbols other than alphanumericals and `_` they are converted to `_`
  * If header is longer than 20 symbols it is cropped to first 18 symbols and dots are added to the end (i.e. `gi|15829254|ref|NC_002695.1` becomes `gi|15829254|ref|NC..`)
* annotation with Prokka 
* fasta files with amino acid sequences are generated from genebank files, gene location and product information is added to headers
* orthogroups inferred with OrthoFinder  
 

