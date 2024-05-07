#!/usr/bin/python3

import sys
import gzip
from Bio import SeqIO

def fastq_to_fasta(input_fastq, output_fasta):
    # Determine if the input and output should be treated as gzipped based on file extension
    if input_fastq.endswith(".gz"):
        fastq_open = gzip.open
    else:
        fastq_open = open

    if output_fasta.endswith(".gz"):
        fasta_open = gzip.open
    else:
        fasta_open = open

    with fastq_open(input_fastq, "rt") as fastq_file, fasta_open(output_fasta, "wt") as fasta_file:
        records = SeqIO.parse(fastq_file, "fastq")
        for rec in records:
            SeqIO.write(rec , fasta_file, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("************************************************************************")
        print("Usage: python fastq2fasta.py <input_fastq> <output_fasta>")
        print("************************************************************************")
        sys.exit(1)

    input_fastq = sys.argv[1]
    output_fasta = sys.argv[2]
    fastq_to_fasta(input_fastq, output_fasta)
