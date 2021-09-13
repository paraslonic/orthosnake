# OrthoRax
This is a pipeline that creates orthogroup fasta files from files with complete genomes, and then runs a generax on these og fasta files. 

It annotate genome with the prokka first, then in runs orthofinder, separates genomes to orthogroups files, and then it runs the GeneRax 

# Requires
Requires [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) and [conda3](https://conda.io/en/latest/) to be installed.\
Please place fasta formated genomes (with .fna extension) in the genomes_input folder.\
Run with `snakemake --use-conda`

If genome files have extension other than .fna please rename them, i.e. with following command:
`for i in genomes_input/*.fasta; do mv $i genomes_input/$(basename $i .fasta).fna; done`$

test_fna folder contains three example sequences of *E. coli* plasmids, which may be used for testing the pipeline. 


# Algorightm
## SnakefileOG file
* Fasta formated files are modified if neccessary to be consisten with prokka annotation tool.  
  * If header contains symbols other than alphanumericals and `_` they are converted to `_`
  * If header is longer than 20 symbols it is cropped to first 18 symbols and dots are added to the end (i.e. `gi|15829254|ref|NC_002695.1` becomes `gi|15829254|ref|NC..`)
* annotation with Prokka 
* fasta files with amino acid and nucleotide sequences are generated from genebank files, gene location and product information is added to headers
* orthogroups inferred with OrthoFinder using amino acid sequences

## SnakefileGR file
* It creates list of required orthogroups using orthogroups.txt file
* It concatenate all annotated genomes to one file 'all_genomes_{aa or nt}.fasta'
* It split the all_genomes files to orthogroup fasta files Orthogroups.txt, all_genomes files, list of required ogs. It split both nt and aa all_genomes files
* It aligns the amino acids fasta files with muscle
* it the aligns nt files over the aligned aa files
* Than it makes files that required for the generax: maps files and a family file
* it runs generax on og_nt_fasta files

 

