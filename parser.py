import re
import csv
from datetime import datetime


kernel_log_pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+(\w+):\s+\[([\d\s.]+)\]\s+(.*)$'
dmesg_log_pattern = re.compile(r'(\w+)\s*:\s*(\w+)\s*:\s*\[(.*?)\]\s*(.*)')


def dmesg_parser(log_file_path, csv_file_path = "./parsed_log_data.csv"):
    with open(log_file_path, 'r') as infile, open(csv_file_path, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Facility', 'Severity', 'Timestamp', 'Message'])  # CSV Header

        for line in infile:
            match = dmesg_log_pattern.match(line.strip())
            if match:
                facility, severity, timestamp, message = match.groups()
                parsed_entry = facility, severity, timestamp, message
            if parsed_entry:
                csv_writer.writerow(parsed_entry)


def kernel_parser(log_file_path, csv_file_path = "./parsed_log_data.csv"):
    # Open the log file and the output CSV file
    with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header row
        header = ['Timestamp', 'Hostname', 'Process', 'Time_since_boot', 'Module', 'Message']
        csv_writer.writerow(header)

        # Parse each log line and write it to the CSV file
        for line in log_file:
            # Define the regular expression pattern
            match = re.match(kernel_log_pattern, line.strip())

            if match:
                try:
                    # Extract the fields
                    date_time_str = match.group(1)
                    hostname = match.group(2)
                    process = match.group(3)
                    time_since_boot_str = match.group(4).replace(' ', '')
                    message = match.group(5)

                    # Parse the time since boot
                    time_since_boot = "{:>9}".format(time_since_boot_str)

                    parsed_line = [date_time_str, hostname, process, time_since_boot, 'kernel', message]
                except ValueError:
                    # Skip malformed lines
                    print(f"Skipping malformed line: {line}")
            else:
                # Skip lines that don't match the pattern
                print(f"Skipping line: {line}")

            if parsed_line:
                csv_writer.writerow(parsed_line)


def parse_syslogs(log_file_path, csv_file_path = "./parsed_log_data.csv"):
    # Open the log file for reading
    with open(log_file_path, 'r') as log_file:
        # Open the output CSV file for writing
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['Date', 'Time', 'Host', 'Process', 'PID', 'Message']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Iterate over each line in the log file
            for line in log_file:
                parts = line.strip().split()
                if len(parts) >= 6:
                    date_parts = parts[0:3]
                    log_date = ' '.join(date_parts[0:2])
                    log_time = date_parts[2]
                    host = parts[3]
                    process_pid = parts[4]
                    message = ' '.join(parts[5:])

                    process, pid = process_pid.split('[')
                    pid = pid.rstrip(']') if pid else ''

                    # Parse the date and time
                    log_datetime = datetime.strptime(f"{log_date} {log_time}", "%b %d %H:%M:%S")

                    # Write the log entry to the CSV file
                    writer.writerow({
                        'Date': log_datetime.date().strftime("%b %d"),
                        'Time': log_datetime.time(),
                        'Host': host,
                        'Process': process,
                        'PID': pid.rstrip(']:'),  # Remove the closing bracket from the PID
                        'Message': message
                    })
    print("Successfully parsed Sys-logs")


def ovs_parser(log_file_path, csv_file_path = "./parsed_log_data.csv"):
    # Open the log file and the output CSV file
    with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header row
        header = ['Timestamp', 'Sequence No', 'Module', 'Log Level', 'Message']
        csv_writer.writerow(header)

        # Parse each log line and write it to the CSV file
        for line in log_file:
            # Split the line into parts
            parts = line.strip().split('|')

            # Parse the timestamp
            timestamp_str = parts[0]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')

            formatted_timestamp = '{}.{:03d}'.format(timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                     int(timestamp.strftime('%f')) // 1000)

            # Extract other fields
            sequence_no = parts[1]
            module = parts[2]
            log_level = parts[3]
            message = '|'.join(parts[4:])

            parsed_line = [formatted_timestamp, sequence_no, module, log_level, message]
            csv_writer.writerow(parsed_line)

    print("Successfully parsed OVS logs")


def parse_log(input_file_path):
    type_of_log, msg = None, 'success'

    with open(input_file_path) as input_file:
        first_line = input_file.readline()


    if re.match(kernel_log_pattern, first_line.strip()):
        type_of_log = 'Kernel'
        print("Detected Kernel Log.")
        try:
            kernel_parser(input_file_path)
        except:
            msg = "ERR"

    elif dmesg_log_pattern.match(first_line.strip()):
        type_of_log = 'DMESG'
        print("Detected DMESG Log.")
        try:
            dmesg_parser(input_file_path)
        except:
            msg = "ERR"

    elif len(first_line.strip().split('|')) == 5:
        type_of_log = 'OVS'
        print("Detected OVS Logs")
        try:
            ovs_parser(input_file_path)
        except:
            msg = "ERR"

    elif len(first_line.strip().split()) >= 6:
        try:
            parse_syslogs(input_file_path)
            type_of_log = 'Sys'
            print("Detected SysLog")
        except:
            msg = 'ERR'

    else:
        print("Not a log.")
        return None, None

    return type_of_log, msg


# Testing .....

# parse_log("./Parsers/kernel_logs.txt")
# parse_log("./Parsers/demo.txt")
# parse_log("./Parsers/ovs-logs.txt")
