import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run bbduk.sh with specified parameters.")
    parser.add_argument("sample_id", help="Sample ID to process")
    parser.add_argument("--bbmappath", required=True, help="Base path to the BBMap software")
    return parser.parse_args()

def construct_command(args):
    bbmappath = args.bbmappath
    sample_id = args.sample_id
    return (f"{bbmappath}/bbmap/bbduk.sh -in1={sample_id}_index.fastq.gz in2={sample_id}_index.fastq.gz "
            f"out1={sample_id}_index.unmapedphix.fastq.gz out2={sample_id}_index.unmapedphix.fastq.gz "
            f"outm1={sample_id}_index.mappedphix.fastq.gz outm2={sample_id}_index.mappedphix.fastq.gz "
            f"ref={bbmappath}/bbmap/resources/phix_adapters.fa.gz k=31 hdist=2 stats=stats.txt")

def run_command(command):
    os.system(command)

def main():
    args = parse_arguments()
    command = construct_command(args)
    run_command(command)

if __name__ == "__main__":
    main()
