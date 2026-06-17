package main

import (
	"flag"

	"github.com/emilykmarx/conftamer/contexttrack"
)

/* Dynamically track context during tests. */

func main() {
	var dlv_port int
	var test_pkg, test_name string
	flag.IntVar(&dlv_port, "dlv-port", 4040, "Listening port for dlv")
	flag.StringVar(&test_pkg, "test-pkg", "", "Package of test to run")
	flag.StringVar(&test_name, "test-name", "", "Name of test to run")
	flag.Parse()

	if err := contexttrack.Run(dlv_port, test_pkg, test_name, 5, func(string, any) error { return nil }); err != nil {
		panic(err)
	}
}
