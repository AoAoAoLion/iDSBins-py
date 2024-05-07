from Bio import Align

aligner = Align.PairwiseAligner()

aligner.mode = "global"
aligner.match_score = 1
aligner.mismatch_score = -1
aligner.gap_score = -0.5


alignments = aligner.align("ACCGT", "ACCCT")

for alignment in alignments:
    print(alignment)

