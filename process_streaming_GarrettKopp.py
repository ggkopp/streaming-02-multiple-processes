# Import from Python Standard Library
import csv
import socket
import time
import logging

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Declare program constants
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "PS4_GamesSales.csv"

# Specify the output file name
OUTPUT_FILE_NAME = "out9.txt"

def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Game, Year, Genre, Publisher, North_America, Europe, Japan, Rest_of_World, Global = row
    fstring_message = f"[{Game},{Year}, {Genre}, {Publisher}, {North_America}, {Europe}, {Japan}, {Rest_of_World}, {Global}]"
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE

def stream_row(input_file_name, address_tuple):
    """Read from input file, stream data, and write to an output file."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    with open(input_file_name, "r") as input_file:
        logging.info(f"Opened for reading: {input_file_name}.")
        reader = csv.reader(input_file, delimiter=",")
        header = next(reader)  # Skip header row
        logging.info(f"Skipped header row: {header}")

        # Open the output file for writing
        with open(OUTPUT_FILE_NAME, "w") as output_file:
            logging.info(f"Opened for writing: {OUTPUT_FILE_NAME}.")

            ADDRESS_FAMILY = socket.AF_INET 
            SOCKET_TYPE = socket.SOCK_DGRAM 
            sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
            
            for row in reader:
                MESSAGE = prepare_message_from_row(row)
                sock_object.sendto(MESSAGE, address_tuple)
                logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
                
                # Write the message to the output file
                output_file.write(f"{MESSAGE.decode()}\n")
                output_file.flush()  # Ensure the data is written immediately

                time.sleep(3)  # Wait 3 seconds between messages

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
