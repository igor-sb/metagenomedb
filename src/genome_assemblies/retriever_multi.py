import pycurl


class PyCurl(object):

    def __init__(self, max_redirs=5, conn_timeout=30, timeout=300):
        self.curl_object = pycurl.Curl()
        self.handle.fp = None
        self.handle.setopt(pycurl.FOLLOWLOCATION, 1)
        self.handle.setopt(pycurl.MAXREDIRS, max_redirs)
        self.handle.setopt(pycurl.CONNECTTIMEOUT, conn_timeout)
        self.handle.setopt(pycurl.TIMEOUT, timeout)
        self.handle.setopt(pycurl.NOSIGNAL, 1)


class ParallelDownloader(object):

    def __init__(self, queue, n_parallel):
        self._curlm = pycurl.CurlMulti()
        self._curlm.handles = [PyCurl() for _ in range(n_parallel)]
        self._free_handles = self._curlm.handles[:]
        self._queue = queue
        self.n_processed_urls = 0
        self.n_total_urls = len(queue)
        return self

    def run(self):
        while self.n_processed_urls < self.n_total_urls:
            self.create_handles_for_urls()
            self.start_downloads()
            self.check_succeded_and_failed_downloads()
        self.close_any_active_handles()
        self._curlm.select(1.0)
        return self

    def create_handles_for_urls(self):
        while self._queue and self._free_handles:
            url, filename = self._queue.pop(0)
            curl_handle = self._free_handles.pop()
            curl_handle.fp = open(filename, 'wb')  # noqa: WPS515
            curl_handle.setopt(pycurl.URL, url)
            curl_handle.setopt(pycurl.WRITEDATA, curl_handle.fp)
            self._curlm.add_handle(curl_handle)

    def start_downloads(self):
        while True:
            ret, _ = self._curlm.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break

    def check_succeded_and_failed_downloads(self):
        while True:
            n_urls, succeded_handles, failed_handles = self._curlm.info_read()
            self.free_handles(succeded_handles)
            self.free_handles(failed_handles)
            n_succeded = len(succeded_handles)
            n_failed = len(failed_handles)
            self.n_processed_urls += n_succeded + n_failed
            if n_urls == 0:
                break

    def free_handles(self, handles_list):
        for curl_handle in handles_list:
            curl_handle.fp.close()
            curl_handle.fp = None
            self._curlm.remove_handle(curl_handle)
            self._free_handles.append(curl_handle)

    def close_any_active_handles(self):
        for curl_handle in self._curlm.handles:
            if curl_handle.fp is not None:
                curl_handle.fp.close()
                curl_handle.fp = None
            curl_handle.close()
        self._curlm.close()
        return self
