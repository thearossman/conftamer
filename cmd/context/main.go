package main

import (
	"flag"

	"github.com/emilykmarx/conftamer/contexttrack"
)

/* Dynamically track context during tests.
Expects headless dlv to already be running on test. */

func main() {
	var dlv_port int
	flag.IntVar(&dlv_port, "dlv-port", 4040, "Port dlv is listening on")
	flag.Parse()

	contexttrack.RunClient(dlv_port)
}
