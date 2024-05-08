import os
import argparse
import subprocess
import gzip
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run PEAR with specified parameters.")
    parser.add_argument("--sample_id", required = True, help="Sample ID to process")
    return parser.parse_args()

def construct_command(args):
    sample_id = args.sample_id
    return (f"pear -f {sample_id}_R1_001_index_unmapedphix.fastq.gz -r {sample_id}_R2_001_index_unmapedphix.fastq.gz "
            f"-o {sample_id}_index_unmappedphix_merged -j 4")

def gzip_command(args):
    sample_id = args.sample_id
    return (f"gzip {sample_id}*fastq")

def run_command(command):
    os.system(command)

def merge_unassembled_reads(args):
    sample_id = args.sample_id
    forward_file = f"{sample_id}_index_unmappedphix_merged.unassembled.forward.fasta.gz"
    reverse_file = f"{sample_id}_index_unmappedphix_merged.unassembled.reverse.fasta.gz"

    # Read forward and reverse files
    with gzip.open(forward_file, "rt") as f_fasta, gzip.open(reverse_file, "rt") as r_fasta:
        forward_reads = SeqIO.to_dict(SeqIO.parse(f_fasta, "fasta"))
        reverse_reads = SeqIO.to_dict(SeqIO.parse(r_fasta, "fasta"))

    # Merge reads based on sequence identifier
    merged_reads = []
    for seq_id in forward_reads:
        if seq_id in reverse_reads:
            # 创建一个新的SeqRecord，将正向和反向序列合并
            merged_sequence = forward_reads[seq_id].seq + reverse_reads[seq_id].seq
            record = SeqRecord(merged_sequence, id=seq_id, description="")
            merged_reads.append(record)
            
    return merged_reads

def write_merged_reads(args, merged_reads):
    sample_id = args.sample_id
    output_file = f"{sample_id}_index_unmappedphix_merged.unassembled.merged_by_seqid.fasta.gz"

    # Write merged reads to a gzipped fasta file
    with gzip.open(output_file, "wt") as output_fasta:
        SeqIO.write(records, output_fasta, "fasta")

def main():
    args = parse_arguments()
    command = construct_command(args)
    run_command(command)
    gzip = gzip_command(args)
    run_command(gzip)
    merged_reads = merge_unassembled_reads(args)
    write_merged_reads(args, merged_reads)

if __name__ == "__main__":
    main()
