from opensearchpy import OpenSearch


def create_os_client(
    host: str,
    port: int,
    auth: str,
    verify_certs: bool,
    use_ssl: bool,
    ssl_show_warn: bool,
):
    splitted_auth = auth.split(":")
    if len(splitted_auth) == 2:
        client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=(splitted_auth[0], splitted_auth[1]),
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            ssl_show_warn=ssl_show_warn,
        )
        return client
    else:
        raise ValueError("Auth format should be 'user:password'")
