"""
Constants
"""

# --------------------------------------------
# Breakpoints
# --------------------------------------------

# Inbound request received (HTTP/1.x). Fires once per request
# before any registered handlers. When this is invoked,
# initial request context is already set.
# Takes *http.Request as an argument named `req`.
HTTP_RECEIVE_FUNC = "net/http.serverHandler.ServeHTTP"

# Inbound request received (HTTP/2). The HTTP/2 server never calls
# serverHandler; it spawns a goroutine via runHandler instead.
# Parameters: rw *http2responseWriter, req *Request, handler func(ResponseWriter, *Request)
HTTP_RECEIVE_FUNC_H2 = "net/http.(*http2serverConn).runHandler"

# Outbound request sent. Performs the actual TCP write.
# takes *http.Request as an argument.
HTTP_SEND_FUNC = "net/http.(*Transport).roundTrip"

# Outbound response sent (HTTP/1.x). Server writes HTTP header by
# committing to a status code.
# Takes `w *net/http.response` (unexported type), which
# contains code and original request.
HTTP_RESPONSE_FUNC = "net/http.(*response).WriteHeader"

# Outbound response sent (HTTP/2). HTTP/2 uses a different response
# writer type; the receiver is `w *http2responseWriter` and the status
# code is the explicit `code int` parameter.
# Request fields are under w.rws.req rather than w.req.
HTTP_RESPONSE_FUNC_H2 = "net/http.(*http2responseWriter).WriteHeader"

# Inbound response received.
# Hooks net/http.redirectBehavior, which is called inside (*Client).do for
# every valid HTTP response (200, 4xx, 5xx, …) immediately after send()
# returns. It takes resp *Response as an explicit argument, so the value is
# live at function entry and always readable — no return-value / DWARF
# dead-range issues. Note: network-level failures (connection refused,
# timeout) cause an early return from (*Client).do before this call, so
# those are not captured here.
HTTP_RECV_RESPONSE_FUNC = "net/http.redirectBehavior"


# --------------------------------------------
# Delve configs
# --------------------------------------------

# TODO: what's a reasonable value for this?
# Used to stacktrace the context propagation path.
STACK_DEPTH = 50

# Controls how deeply to inspect variables
LOAD_CFG = {
    # If variable is a pointer, dereference it
    "FollowPointers":     True,
    # Nested structs/interfaces
    "MaxVariableRecurse": 6,
    # Truncate string values
    "MaxStringLen":       512,
    # Truncate array/slice contents
    "MaxArrayValues":     32,
    # Show all struct fields
    "MaxStructFields":    -1,
}

# Concrete types to track for the context.Context interface.
# TODO is this a reasonable set?
CONTEXT_TYPES = {
    "context.Context",
    "context.cancelCtx",        "*context.cancelCtx",
    "context.timerCtx",         "*context.timerCtx",
    "context.valueCtx",         "*context.valueCtx",
    "context.emptyCtx",         "*context.emptyCtx",
    "context.backgroundCtx",    "*context.backgroundCtx",
    "context.todoCtx",          "*context.todoCtx",
    "context.withoutCancelCtx", "*context.withoutCancelCtx",
}