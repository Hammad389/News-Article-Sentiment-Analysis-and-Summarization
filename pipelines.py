During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\cache.py", line 198, in run_and_cache
    result = cast(T, self.get(namespace=namespace, key=key_args))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\cache.py", line 101, in get
    raise KeyError("namespace: " + namespace + " key: " + repr(key))
KeyError: "namespace: urls key: {'url': 'https://publicsuffix.org/list/public_suffix_list.dat'}"

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connectionpool.py", line 464, in _make_request
    self._validate_conn(conn)
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connectionpool.py", line 1093, in _validate_conn
    conn.connect()
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connection.py", line 741, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connection.py", line 920, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
               ^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\util\ssl_.py", line 480, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\util\ssl_.py", line 524, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ProgramData\anaconda3\Lib\ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ProgramData\anaconda3\Lib\ssl.py", line 1041, in _create
    self.do_handshake()
  File "C:\ProgramData\anaconda3\Lib\ssl.py", line 1319, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connectionpool.py", line 488, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\urllib3\util\retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='publicsuffix.org', port=443): Max retries exceeded with url: /list/public_suffix_list.dat (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\suffix_list.py", line 46, in find_first_response
    return cache.cached_fetch_url(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\cache.py", line 209, in cached_fetch_url
    return self.run_and_cache(
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\cache.py", line 200, in run_and_cache
    result = func(**kwargs)
             ^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\tldextract\cache.py", line 218, in _fetch_url
    response = session.get(url, timeout=timeout)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\requests\sessions.py", line 602, in get
    return self.request("GET", url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\requests\adapters.py", line 698, in send
    raise SSLError(e, request=request)
