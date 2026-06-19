"""
Printing and data-collection helpers for HTTP messages.
Each function prints the message to the terminal and returns its fields as a dict.
"""

from delve_client_rpc import *


def _eval_flat(client: DelveClient, goroutine_id: int, frame: int, expr: str) -> str:
    try:
        return flat_value(client.eval_variable(goroutine_id, frame, expr).get("Variable") or {})
    except Exception as e:
        return f"<error: {e}>"


def _print_and_collect(client, goroutine_id, header, exprs) -> dict:
    print(f"\n┌─ {header}")
    data = {}
    for expr in exprs:
        val = _eval_flat(client, goroutine_id, 0, expr)
        data[expr] = val
        print(f"│  {expr:<26} = {val}")
    print("└──────────────────────────────────────────────────────────────")
    return data


def get_http_request_recvd(client: DelveClient, goroutine_id: int) -> dict:
    return _print_and_collect(client, goroutine_id,
        "HTTP Request (received by server) ─────────────────────────",
        ["req.Method", "req.URL.Path", "req.URL.RawQuery", "req.Header", "req.RemoteAddr", "req.Proto"])


def get_http_request_sent(client: DelveClient, goroutine_id: int) -> dict:
    return _print_and_collect(client, goroutine_id,
        "HTTP Request (message being sent) ─────────────────────────",
        ["req.Method", "req.URL.Scheme", "req.URL.Host", "req.URL.Path", "req.URL.RawQuery", "req.Header"])


def get_http_response_sent(client: DelveClient, goroutine_id: int) -> dict:
    return _print_and_collect(client, goroutine_id,
        "HTTP Response (message being sent, HTTP/1.x) ──────────────",
        ["code", "w.handlerHeader", "w.req.Method", "w.req.URL.Path", "w.req.URL.RawQuery"])


def get_http_response_sent_h2(client: DelveClient, goroutine_id: int) -> dict:
    # For HTTP/2, the receiver is *http2responseWriter and request fields
    # live at w.rws.req rather than w.req.
    return _print_and_collect(client, goroutine_id,
        "HTTP Response (message being sent, HTTP/2) ────────────────",
        ["code", "w.rws.handlerHeader", "w.rws.req.Method", "w.rws.req.URL.Path", "w.rws.req.URL.RawQuery"])


def get_http_response_recvd(client: DelveClient, goroutine_id: int) -> dict:
    print("\n┌─ HTTP Response (received) ───────────────────────────────────")
    all_vars = get_all_frame_vars(client, goroutine_id, 0)
    resp_var = next(
        (v for v in all_vars if v.get("type") in ("*net/http.Response", "net/http.Response")),
        None,
    )
    if resp_var is None:
        print("│  (no *http.Response variable found in frame 0)")
        print("└──────────────────────────────────────────────────────────────")
        return {}
    vname = resp_var.get("name", "")
    data = {}
    for field in ["Status", "StatusCode", "Proto", "Header"]:
        val = _eval_flat(client, goroutine_id, 0, f"{vname}.{field}")
        data[f"resp.{field}"] = val
        print(f"│  resp.{field:<21} = {val}")
    print("└──────────────────────────────────────────────────────────────")
    return data
