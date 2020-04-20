GENOMES, = glob_wildcards("fna/{genome}.fna")


rule all:
	input: 
		"Results/Orthogroups.txt"

rule orthofinder:
	input: 
		expand("faa/{genome}.fasta", genome=GENOMES)
	output:
		"Results/Orthogroups.txt"
	threads: 50
	conda: "envs/ortho.yaml"
	log: "log_of.txt"
	shell:
		"bash scripts/run_orthofinder.sh {threads} > {log}"
rule prokka:
	input: "fna/{genome}.fna"
	output:
		"prokka/{genome}/{genome}.gbk"
	threads: 4
	conda: "envs/prokka.yaml"
	shell:
		"""
		prokka --cpus {threads} --outdir prokka/{wildcards.genome} --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input} 2>/dev/null
		#cp prokka/{wildcards.genome}/{wildcards.genome}.gbf prokka/{wildcards.genome}/{wildcards.genome}.gbk 2>/dev/null
		"""

rule make_faa:
	input:	"prokka/{genome}/{genome}.gbk"
	output: "faa/{genome}.fasta"
	conda: "envs/scripts.yaml"
	shell:
		"name=$(basename {input});"
		"python3 scripts/GBfaa.py -gb  {input} > {output}"
