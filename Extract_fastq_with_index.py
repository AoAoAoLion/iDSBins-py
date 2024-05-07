from Bio import SeqIO
import argparse
"""
# README:
# This script is designed to process paired-end FASTQ files by filtering reads based on provided index sequences.
# It takes forward and reverse FASTQ files as input along with the corresponding forward and reverse index sequences.
# The script outputs two sets of FASTQ files:
# 1. Reads where both the forward and reverse reads start with the specified indices.
# 2. Reads where either the forward or reverse read does not start with the specified indices.
#
# Usage:
# python Extract_fastq_with_index.py -f <forward.fastq> -r <reverse.fastq> -i <forward_index> -g <reverse_index> -o <output_prefix>
#
# Arguments:
# -f, --ffastq: Forward reads file in FASTQ format.
# -r, --Rfastq: Reverse reads file in FASTQ format.
# -i, --forward_index: Index sequence at the start of the forward reads.
# -g, --reverse_index: Index sequence at the start of the reverse reads.
# -o, --output: Prefix for the output files.
#
# Output files:
# <output_prefix>.R1.fastq: Forward reads with correct index.
# <output_prefix>.R2.fastq: Reverse reads with correct index.
# <output_prefix>.unindex.R1.fastq: Forward reads without correct index.
# <output_prefix>.unindex.R2.fastq: Reverse reads without correct index.
"""


def print_help():
    print("""
    Usage:
        python Extract_fastq_with_index.py -f <forward.fastq> -r <reverse.fastq> -i <forward_index> -g <reverse_index> -o <output_prefix>

    Description:
        This script processes paired-end FASTQ files by filtering reads based on provided index sequences. It outputs two sets of FASTQ files:
        1. Reads where both the forward and reverse reads start with the specified indices.
        2. Reads where either the forward or reverse read does not start with the specified indices.

    Arguments:
        -f, --ffastq: Forward reads file in FASTQ format.
        -r, --Rfastq: Reverse reads file in FASTQ format.
        -i, --forward_index: Index sequence at the start of the forward reads.
        -g, --reverse_index: Index sequence at the start of the reverse reads.
        -o, --output: Prefix for the output files.

    Output files:
        <output_prefix>.R1.fastq: Forward reads with correct index.
        <output_prefix>.R2.fastq: Reverse reads with correct index.
        <output_prefix>.unindex.R1.fastq: Forward reads without correct index.
        <output_prefix>.unindex.R2.fastq: Reverse reads without correct index.
    """)


def parse_args():
    parser = argparse.ArgumentParser(description='Process FASTQ files.')
    parser.add_argument('-f', '--ffastq', required=True, help='Forward reads (FASTQ format)')
    parser.add_argument('-r', '--Rfastq', required=True, help='Reverse reads (FASTQ format)')
    parser.add_argument('-i', '--forward_index', required=True, help='Forward index')
    parser.add_argument('-g', '--reverse_index', required=True, help='Reverse index')
    parser.add_argument('-o', '--output', required=True, help='Output file prefix')
    return parser.parse_args()

def main():
    args = parse_args()
    # If the user needs help, print the detailed help information
    if args.help:
        print_help()
        return
    # Open input FASTQ files
    forward_reads = SeqIO.parse(args.ffastq, "fastq")
    reverse_reads = SeqIO.parse(args.Rfastq, "fastq")

    # Open output files
    with open(args.output + '.R1.fastq', 'w') as pair1, \
         open(args.output + '.R2.fastq', 'w') as pair2, \
         open(args.output + '.unindex.R1.fastq', 'w') as upair1, \
         open(args.output + '.unindex.R2.fastq', 'w') as upair2:

        # Process each pair of reads
        for read1, read2 in zip(forward_reads, reverse_reads):
            if read1.seq.startswith(args.forward_index) and read2.seq.startswith(args.reverse_index):
                SeqIO.write(read1, pair1, "fastq")
                SeqIO.write(read2, pair2, "fastq")
            else:
                SeqIO.write(read1, upair1, "fastq")
                SeqIO.write(read2, upair2, "fastq")

if __name__ == "__main__":
    main()