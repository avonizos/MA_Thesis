from lingpy import *
from lingpy.evaluate import alr

d = get_wordlist('data.csv', delimiter='\t')
tree = Tree(d.get_tree())
print(tree.asciiArt())

d = get_wordlist('data1.csv', delimiter='\t')
tree = Tree(d.get_tree())
print(tree.asciiArt())
# seqs = d.ipa
# msa = Multiple(seqs)
# msa.prog_align()
# m = alr.mean_edit_distance(d,gold='proto', test='consensus', ref='cogid', tokens=True, classes=False)
# print m