#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

#
# Usage: python retriever-multi.py <file with URLs to fetch> [<# of
#          concurrent connections>]
#

import sys
import signal
import pycurl

# We should ignore SIGPIPE when using pycurl.NOSIGNAL - see
# the libcurl tutorial for more info.
# try:
#     import signal
#     from signal import SIGPIPE, SIG_IGN
# except ImportError:
#     pass
# else:
#     signal.signal(SIGPIPE, SIG_IGN)


# sys.argv[1] = 

# Get args
num_conn = 10
# try:
#     if sys.argv[1] == "-":
#         urls = sys.stdin.readlines()
#     else:
#         urls = open(sys.argv[1]).readlines()
#     if len(sys.argv) >= 3:
#         num_conn = int(sys.argv[2])
# except:
#     print("Usage: %s <file with URLs to fetch> [<# of concurrent connections>]" % sys.argv[0])
#     raise SystemExit



# Make a queue with (url, filename) tuples
# queue = []
# for url in urls:
#     url = url.strip()
#     if not url or url[0] == "#":
#         continue
#     filename = "doc_%03d.dat" % (len(queue) + 1)
#     queue.append((url, filename))



def create_download_list(
    assembly_summary_filename: str,
    output_path: str = 'data/',
):
    df = load_preprocessed_assembly_summary_table(assembly_summary_filename)
    df.url_features
    df.url_sequence




# Check args
assert queue, "no URLs given"
n_total_urls = len(queue)
num_conn = min(num_conn, num_urls)
assert 1 <= num_conn <= 10000, "invalid number of concurrent connections"
print("PycURL %s (compiled against 0x%x)" % (pycurl.version, pycurl.COMPILE_LIBCURL_VERSION_NUM))
print("----- Getting", num_urls, "URLs using", num_conn, "connections -----")


def preallocate_curl_handles():
    multicurl = pycurl.CurlMulti()
    multicurl.handles = []
    for i in range(num_conn):
        curl_handle = pycurl.Curl()
        curl_handle.fp = None
        curl_handle.setopt(pycurl.FOLLOWLOCATION, 1)
        curl_handle.setopt(pycurl.MAXREDIRS, 5)
        curl_handle.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl_handle.setopt(pycurl.TIMEOUT, 300)
        curl_handle.setopt(pycurl.NOSIGNAL, 1)
        multicurl.handles.append(curl_handle)
    return multicurl

multicurl = preallocate_curl_handles()

# Main loop
free_handles = multicurl.handles[:]
n_processed_urls = 0
while n_processed_urls < n_total_urls:
    # If there is an url to process and a free curl object, add to multi stack
    while queue and free_handles:
        url, filename = queue.pop(0)
        curl_handle = free_handles.pop()
        curl_handle.fp = open(filename, "wb")
        curl_handle.setopt(pycurl.URL, url)
        curl_handle.setopt(pycurl.WRITEDATA, c.fp)
        multicurl.add_handle(curl_handle)
        # store some info
        curl_handle.filename = filename
        curl_handle.url = url
    # Run the internal curl state machine for the multi stack
    while 1:
        ret, num_handles = multicurl.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM:
            break
    # Check for curl objects which have terminated, and add them to the freelist
    while 1:
        n_terminated, success_handles, failed_handles = multicurl.info_read()
        # Remove success_handles from the multicurl and add them to the free_handles
        def free_success_handles(multicurl, success_handles, free_handles):            
            for curl_handle in success_handles:
                curl_handle.fp.close()
                curl_handle.fp = None
                multicurl.remove_handle(curl_handle)
                print("Success:", curl_handle.filename, curl_handle.url, curl_handle.getinfo(pycurl.EFFECTIVE_URL))
                free_handles.append(curl_handle)
            return (multicurl, success_handles, free_handles)

        multicurl, success_handles, free_handles = free_success_handles(
            multicurl,
            success_handles,
            free_handles,
        )

        for curl_handle, errno, errmsg in failed_handles:
            curl_handle.fp.close()
            curl_handle.fp = None
            multicurl.remove_handle(curl_handle)
            print("Failed: ", curl_handle.filename, curl_handle.url, errno, errmsg)
            free_handles.append(curl_handle)
        n_processed_urls += len(success_handles) + len(failed_handles)
        if n_terminated == 0:
            break
    # Currently no more I/O is pending, could do something in the meantime
    # (display a progress bar, etc.).
    # We just call select() to sleep until some more data is available.
    multicurl.select(1.0)


# Cleanup
for c in m.handles:
    if c.fp is not None:
        c.fp.close()
        c.fp = None
    c.close()
m.close()

class ParallelDownloader():
    def __init__(self, n_parallel):
        self.n_parallel = n_parallel
        self.multicurl = pycurl.CurlMulti()
        self.multicurl.handles = []
        for i in range(n_parallel):
            curl_handle = pycurl.Curl()
            curl_handle.fp = None
            curl_handle.setopt(pycurl.FOLLOWLOCATION, 1)
            curl_handle.setopt(pycurl.MAXREDIRS, 5)
            curl_handle.setopt(pycurl.CONNECTTIMEOUT, 30)
            curl_handle.setopt(pycurl.TIMEOUT, 300)
            curl_handle.setopt(pycurl.NOSIGNAL, 1)
            multicurl.handles.append(curl_handle)        
        self.free_handles = []
        self.success_handles = []
        self.failed_handles = []
