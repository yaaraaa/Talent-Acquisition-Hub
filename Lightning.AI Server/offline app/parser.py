import os

def parse_pdf(input_folder, output_folder, workers=4):
    """
    Function to parse PDF files in the specified input folder using the marker tool.

    Args:
    - input_folder (str): Path to the folder containing PDF files to parse.
    - output_folder (str): Path to the folder where output should be saved.
    - workers (int): Number of workers to use (default: 4).
    - max_files (int): Maximum number of files to process (default: 10).
    """
    # Make sure the input and output folders are valid directories
    if not os.path.isdir(input_folder):
        raise ValueError(f"Input folder '{input_folder}' is not a valid directory.")
    if not os.path.isdir(output_folder):
        raise ValueError(f"Output folder '{output_folder}' is not a valid directory.")

    # Change directory to the marker folder
    marker_dir = "/teamspace/studios/this_studio/marker"
    os.chdir(marker_dir)

    # Construct the marker command as a string with quoted paths
    command = (
        f"python /teamspace/studios/this_studio/marker/convert.py \"{input_folder}\" --output_dir \"{output_folder}\" "
        f"--workers {workers}"
    )
    print(command)

    try:
        # Execute the command using os.system
        exit_code = os.system(command)
        if exit_code == 0:
            print("PDF parsing completed successfully.")
        else:
            print(f"Marker command failed with exit code: {exit_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

