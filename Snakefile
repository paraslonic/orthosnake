configfile: 'config.yml'

GENOMES, = glob_wildcards("fna/{genome}.fna")

localrules: all,  make_path, calc_complexity

rule all:
	input: 
		"tmp/Orthogroups.txt"

rule orthofinder:
	input: 
		expand("faa/{qu}.fasta", qu=GENOMES)
	output:
		"tmp/Orthogroups.txt"
	threads: 4
	conda: "conda.yaml"
	log: "log_of.txt"
	shell:
		"bash scripts/run_orthofinder.sh {threads} > {log}"
rule prokka:
	input:
		ancient("fna/{qu}.fna")
	output:
		directory("prokka/{qu}")
	threads: 4
	conda: "conda.yaml"
	shell:
		"name=$(basename {input} .fna);"
		"prokka --cpus {threads} --outdir {output} --force --prefix $name --locustag $name {input}"

rule make_faa:
	input:
		ancient("prokka/{qu}")
	output:
		"faa/{qu}.fasta"
	conda: "conda.yaml"
	shell:
		"name=$(basename {input});"
		"{config[python.bin]} scripts/GBfaa.py {input}/$name.gbk > {output}"
