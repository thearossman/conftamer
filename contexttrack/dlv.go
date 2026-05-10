package contexttrack

import (
	"fmt"
	"log"

	"github.com/go-delve/delve/service/rpc2"
)

// Connect to dlv and run the test
func RunClient(dlv_port int) {
	dlv_endpoint := fmt.Sprintf("localhost:%v", dlv_port)
	fmt.Printf("Connecting to dlv on %v\n", dlv_endpoint)

	client := rpc2.NewClient(dlv_endpoint)
	state := <-client.Continue()

	for ; !state.Exited; state = <-client.Continue() {
		if state.Err != nil {
			log.Fatalf("Error in debugger state: %v\n", state.Err)
		}
	}

	fmt.Printf("Target exited with status %v\n", state.ExitStatus)

	client.Detach(false) // Also kills server, despite function doc
}
