GENOMES, = glob_wildcards("tmp/og_aligned_aa/{genome}.fasta")
rule all:
    input: expand("tmp/test2/{genome}.fasta", genome=GENOMES)
rule test:
    input: 'tmp/og_aligned_aa/{genome}.fasta'
    output : 'tmp/test2/{genome}.fasta'
    shell : 'cp {input} {output}'