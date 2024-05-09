#!/usr/bin/python3

import argparse
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
            SeqIO.write(rec, fasta_file, "fasta")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert FASTQ to FASTA")
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ file (optionally gzipped)")
    parser.add_argument("-o", "--output", help="Output FASTA file (optionally gzipped)")
    args = parser.parse_args()

    # Automatically change the output file's suffix if not specified
    if not args.output:
        if args.input.endswith(".gz"):
            args.output = args.input[:-9] + ".fasta.gz"  # Change .fastq.gz to .fasta.gz
        else:
            args.output = args.input[:-6] + ".fasta"  # Change .fastq to .fasta

    fastq_to_fasta(args.input, args.output)
