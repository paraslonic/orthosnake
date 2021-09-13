GENOMES, = glob_wildcards("genomes_input/{genome}.fna")


rule all:
	input: 
		"Results/Orthogroups.txt", expand("tmp/genome_fasta_nt/{genome}.fasta", genome=GENOMES)
    
# Shortens the lengths of headings 
rule check_genomes_input:
	input: "genomes_input/{genome}.fna"
	output: "tmp/genomes_cut/{genome}.fna"
	conda: "envs/scripts.yaml"
	shell:	"python scripts/cropHeader.py -input  {input} -out {output} -n 20"
		
# Annotate genomes
rule prokka:
	input: "tmp/genomes_cut/{genome}.fna"
	output:
		"prokka/{genome}/{genome}.gbk"
	threads: 4
	conda: "envs/prokka.yaml"
	shell:
		"""
		prokka --cpus {threads} --outdir prokka/{wildcards.genome} --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input} 2>/dev/null
		#cp prokka/{wildcards.genome}/{wildcards.genome}.gbf prokka/{wildcards.genome}/{wildcards.genome}.gbk 2>/dev/null
		"""
# Converts a genebank to fasta with a special header. One fasta per genome 
rule make_genome_fasta_aa:
	input:	"prokka/{genome}/{genome}.gbk"
	output: "tmp/genome_fasta_aa/{genome}.fasta"
	conda: "envs/scripts.yaml"
	shell:
		"name=$(basename {input});"
		"python scripts/GB_genome_fasta_aa.py -gb  {input} > {output}"
        
rule make_genome_fasta_nt:
	input:	"prokka/{genome}/{genome}.gbk"
	output: "tmp/genome_fasta_nt/{genome}.fasta"
	conda: "envs/scripts.yaml"
	shell:
		"name=$(basename {input});"
		"python scripts/GB_genome_fasta_nt.py -gb  {input} > {output}"
  
# Takes everything fasta, launches an orthofinder on them 
rule orthofinder:
	input: 
		expand("tmp/genome_fasta_aa/{genome}.fasta", genome=GENOMES)
	output:
		"Results/Orthogroups.txt"
	threads: 50
	conda: "envs/ortho.yaml"
	log: "log_of.txt"
	shell:
		"bash scripts/run_orthofinder.sh {threads} > {log}"
