package tools

import (
	"fmt"
	"log"
	"net/http"
)

var PORT = 8080

func InitWebServer() {
	registerEndpoints()
	fmt.Printf("Server running on port %v\n", PORT)
	if err := http.ListenAndServe("localhost:8081", nil); err != nil {
		log.Fatal(err)
	}
}

func registerEndpoints() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNoContent)
	})
}
