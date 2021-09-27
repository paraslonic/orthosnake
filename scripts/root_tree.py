from Bio import Phylo
from sys import argv
file_input = argv[1] 
file_output = argv[2] 
tree = Phylo.read(file_input, "newick")
tree.root_at_midpoint()
Phylo.write(tree, file_output, "newick")