import pandas as pd
from Bio import Phylo
ogs = pd.read_table('Results/Orthogroups.txt', sep = ':', header=None)
ogs = list(ogs[0])


rule all:
    input: 'Results/geneRaxResults'

rule create_og_list:
    input: 'Results/Orthogroups.txt'
    output: "tmp/list_of_ogs.txt"
    run:
        import pandas as pd
        ogs = pd.read_table(str(input), sep = ':', header=None)
        ogs = list(ogs[0])
        with open(str(output), "w") as handle:
            for og in ogs:
                handle.write((og + "\n"))

rule catGenomes:
    output: 'tmp/all_genomes_aa.fasta', 'tmp/all_genomes_nt.fasta'
    shell: 
        '''
        cat tmp/genome_fasta_aa/*.fasta > {output[0]}
        cat tmp/genome_fasta_nt/*fasta > {output[1]}
        '''
rule splitToOg_nt:
    input: 'Results/Orthogroups.txt', 'tmp/all_genomes_nt.fasta', "tmp/list_of_ogs.txt"
    output: expand('tmp/ogs_nt_fasta/{og}.fasta', og=ogs)
    shell:
        '''
        python scripts/splitToOg.py {input[0]} {input[1]} {input[2]} tmp/ogs_nt_fasta/
        '''
rule splitToOg_aa:
    input: 'Results/Orthogroups.txt', 'tmp/all_genomes_aa.fasta', "tmp/list_of_ogs.txt"
    output: expand('tmp/ogs_aa_fasta/{og}.fasta', og=ogs)
    shell:
        '''
        python scripts/splitToOg.py {input[0]} {input[1]} {input[2]} tmp/ogs_aa_fasta/
        '''
        
rule align_amino_acids:
    input: 'tmp/ogs_aa_fasta/{og}.fasta'
    output: 'tmp/ogs_aa_aligned_fasta/{og}.fasta'
    conda: 'envs/muscle.yaml'
    shell:
        '''
        muscle -in {input} -out {output}
        '''
rule align_nt:
    input: 
        nt = 'tmp/ogs_nt_fasta/{og}.fasta',
        aa = 'tmp/ogs_aa_aligned_fasta/{og}.fasta'
    output: 
        'Results/ogs_nt_aligned_fasta/{og}.fasta'
    shell:
        '''
        python scripts/GapsFromAA.py {input.nt} {input.aa} {output}
        '''

def aggregate_input(wildcards):
    ogs = list(pd.read_csv('Results/Orthogroups_SingleCopyOrthologues.txt', header = None).iloc[:, 0])
    ogs = ['tmp/ogs_aa_aligned_fasta/' + x + '.fasta' for x in ogs]
    return ogs

rule cat_core:
    input: aggregate_input
    output: "tmp/coreogaligned.fasta"
    conda: "envs/scripts_tree.yaml"
    shell:
        "echo {input};"
        "python scripts/concatenate.py {input} {output}"

rule tree_for_core:
    input: rules.cat_core.output
    threads: 4
    output:
        "Results/coreogs_nucleotide.treefile"
    shell:
        """
        iqtree -s {input} -nt {threads} -pre Results/coreogs_nucleotide -redo -m MFP
        """
rule midpoint_root:
    input: 'Results/coreogs_nucleotide.treefile'
    output: 'Results/rooted_tree.nwk'
    conda: "envs/scripts.yaml"
    shell:
        '''
        python scripts/root_tree.py {input} {output}
        '''

rule make_maps_file:
    input: 'Results/ogs_nt_aligned_fasta/{og}.fasta'
    output : 'tmp/map_files/{og}.txt'
    shell:
        '''
        python scripts/crMapFile.py {input} {output}
        '''
rule make_families_file:
    input:
        files = expand('tmp/map_files/{og}.txt', og=ogs)
    output:
        'tmp/familiesFile.txt'
    shell:
        '''
        python scripts/crFamiliesFile.py Results/ogs_nt_aligned_fasta/ tmp/map_files/ {output}
        '''        

rule run_generax:
    input: 
        famfile='tmp/familiesFile.txt',
        tree='Results/rooted_tree.nwk'
    output: directory('Results/geneRaxResults')
    conda: 'envs/generax.yaml'
    threads: 4
    shell:'mpiexec -np 10 generax -f {input.famfile} -s {input.tree} -p {output}'