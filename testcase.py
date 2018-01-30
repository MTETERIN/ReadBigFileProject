import re
import time


def log_calltime(func):
    """Return a function call time

    Decorator to log call time for the method.

    """
    def calc_time(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            print("Call time - %s - %.1f s" % (
                func.__name__, (time.time() - start)))
    return calc_time


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_data(piece, ipv4):
    ip_pattern = re.compile('((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)')
    ip_iterator = ip_pattern.finditer(piece)
    for ip_match in ip_iterator:
        if ip_match is not ipv4:
            ipv4.add(ip_match.group())


@log_calltime
def find_unique_ip(data_path):
    """Form all unique ips.

    Keyword arguments:
    data_path --data path of file

    """
    try:
        ipv4 = set()
        file_handler = open(data_path,"r")
        for piece in read_in_chunks(file_handler):
            process_data(piece, ipv4)

    except IOError as ioe:
        print("An IOError has occurred! " + str(ioe) )
    except Exception as e:
        print("Error! " + str(e))
    finally:
        file_handler.close()
    return ipv4;


if __name__ == '__main__':
    file_name = input("Enter file name: ");
    ipv4 = find_unique_ip(file_name)
    print(ipv4)
