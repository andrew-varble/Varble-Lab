import csv
import re

def calculate_alignment_length(cigar_string):
    """Calculate the alignment length from the CIGAR string."""
    cigar_operations = re.findall(r'(\d+)([MIDNSHP=X])', cigar_string)
    alignment_length = 0

    for length, operation in cigar_operations:
        length = int(length)
        if operation in ('M', 'D', 'N', '=', 'X'):
            alignment_length += length

    return alignment_length

def extract_aligned_reads_to_csv(input_sam, output_csv, num_reads=1000, min_read_length=1200):
    # Open the input SAM file
    with open(input_sam, 'r') as infile:
        # Open the CSV file for writing
        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(['Full Read Sequence', 'Alignment Length', 'Start Position', 'Full Read Length'])

            # Initialize a counter for the number of aligned reads
            aligned_read_count = 0

            # Read through the input SAM file line by line
            for line in infile:
                # Skip header lines
                if line.startswith('@'):
                    continue

                # Split the line into columns
                columns = line.split('\t')

                # Extract relevant fields
                flag = int(columns[1])
                start_position = int(columns[3])
                cigar_string = columns[5]
                sequence = columns[9]

                # Check if the read is aligned (flag 4 means the read is unmapped)
                if flag & 4 == 0:
                    alignment_length = calculate_alignment_length(cigar_string)
                    sequence_length = len(sequence)

                    # Check if the read length is greater than the specified minimum length
                    if sequence_length > min_read_length:
                        # Write the read information to the CSV
                        csv_writer.writerow([sequence, alignment_length, start_position, sequence_length])

                        # Increment the count of aligned reads
                        aligned_read_count += 1

                # Stop after writing the specified number of aligned reads
                if aligned_read_count >= num_reads:
                    break

# Example usage
input_sam_path = 'obelisk_10.sam'
output_csv_path = 'aligned_reads_10.csv'
extract_aligned_reads_to_csv(input_sam_path, output_csv_path)
