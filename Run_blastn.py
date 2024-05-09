import os
import argparse
import gzip
import shutil

def construct_command(query_file, database, output_file, blastn_path, num_threads=1):
    # Construct the BLASTN command
    return(f'{blastn_path} -query {query_file} -out {output_file}  -db {database} -num_threads {num_threads}  -outfmt '
           f'"6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen bitscore evalue" ' 
           f'-max_target_seqs 1')

def decompress_gzip_file(gzip_path, decompressed_path):
    with gzip.open(gzip_path, 'rb') as f_in:
        with open(decompressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def compress_file(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="运行BLASTN对指定数据库进行搜索")
    parser.add_argument("--query", required=True, help="查询文件的路径")
    parser.add_argument("--database", required=True, help="BLAST数据库的路径")
    parser.add_argument("--output", required=True, help="输出结果文件的路径")
    parser.add_argument("--blastn_path", default="blastn", help="BLASTN可执行文件的路径")
    parser.add_argument("--num_threads", type=int, default=1, help="使用的线程数，默认为1")

    # Parse arguments
    args = parser.parse_args()

    # Decompress query file if it is a gzip file
    decompressed_query = None
    if args.query.endswith('.gz'):
        decompressed_query = args.query.rstrip('.gz')
        decompress_gzip_file(args.query, decompressed_query)
        args.query = decompressed_query

    # Run BLASTN with the provided arguments
    blastn_run_command = construct_command(args.query, args.database, args.output, args.blastn_path, args.num_threads)
    print(blastn_run_command)
    os.system(blastn_run_command)

    # Compress the output file
    compress_file(args.output, args.output + '.gz')

    # Remove the original output file
    os.remove(args.output)

    # Remove the decompressed file if it was created
    if decompressed_query:
        os.remove(decompressed_query)

if __name__ == "__main__":
    main()