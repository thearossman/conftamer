// Minimal smoke test for HTTP/2 Delve breakpoints.
// Run under Delve to verify that net/http.(*http2serverConn).runHandler
// and net/http.(*http2responseWriter).WriteHeader fire.
//
// Terminal 1:
//
//	dlv test --headless --listen=:2345 --api-version=2 \
//	    github.com/emilykmarx/conftamer/contexttrack \
//	    -- -test.run TestH2Smoke -test.v -test.timeout 120s
//
// Terminal 2:
//
//	python3 delve_client.py --output /tmp/h2smoke.jsonl
package contexttrack

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestH2Smoke(t *testing.T) {
	srv := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Proto", r.Proto)
		w.WriteHeader(http.StatusOK)
		io.WriteString(w, "hello")
	}))
	srv.EnableHTTP2 = true
	srv.StartTLS()
	defer srv.Close()

	// srv.Client() is pre-configured with the test CA and HTTP/2 enabled.
	resp, err := srv.Client().Get(srv.URL + "/hello")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	t.Logf("proto=%s status=%s", resp.Proto, resp.Status)

	if resp.Proto != "HTTP/2.0" {
		t.Errorf("expected HTTP/2.0, got %s", resp.Proto)
	}
}
