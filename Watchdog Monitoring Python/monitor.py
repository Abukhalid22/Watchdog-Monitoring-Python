import getpass  # Library to get the current user's username
import logging  # Library for logging
import os  # Library for file and directory operations
import shutil  # Library for file copying
import sys  # Library for system-specific parameters and functions
import time  # Library for time-related functions

from watchdog.events import LoggingEventHandler  # Watchdog event handler for logging
from watchdog.observers import (
    Observer,  # Watchdog observer for monitoring file system events
)


# Function to backup the directory by copying from one folder to another if there is a modification
def on_modified(event):
    """Backup the directory by copying from one folder to another if there is a modification"""
    backup_path = '/mnt/c/Users/nasir/OneDrive/Desktop/tuts/BACKUP/'  # Destination folder for backup
    # Fetch all files in the path (source directory)
    for file_name in os.listdir(path):
        # Construct full file paths for source and destination
        source = path + file_name  # Path to the file in the source directory
        destination = backup_path + file_name  # Path to the same file in the backup directory
        # Copy the files if they are regular files (not directories)
        if os.path.isfile(source):
            shutil.copy(source, destination)  # Copy the file from source to destination
            print(f"Copied: {file_name}")  # Print a message indicating that the file was copied


if __name__ == '__main__':
    # How to store logs to a file and include the username
    user = getpass.getuser()  # Get the current username
    logging.basicConfig(filename='dev.log', filemode='a', level=logging.INFO,
                        format='%(asctime)s | %(process)d | %(message)s' + f' | By Following Userid: {user}',
                        datefmt='%Y-%m-%d %H:%M:%S')  # Configure logging to write to 'dev.log' with user-specific information
    # Directory or file that you want to monitor (can be provided as a command-line argument)
    path = sys.argv[1] if len(sys.argv) > 1 else '.'  # Use the provided path or the current directory if not specified
    event_handler = LoggingEventHandler()  # Create a Watchdog event handler for logging
    event_handler.on_modified = on_modified  # Set the on_modified method to the custom backup function
    observer = Observer()  # Create a Watchdog observer
    observer.schedule(event_handler, path, recursive=True)  # Configure the observer to watch for events in the specified path
    observer.start()  # Start the observer to monitor the specified path

    try:
        while True:
            time.sleep(1)  # Keep the script running to continuously monitor the directory
    except KeyboardInterrupt:
        observer.stop()  # Stop the observer if a keyboard interrupt is detected
        observer.join()  # Wait for the observer to finish before exiting the program
