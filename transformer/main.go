package main

import (
	"fmt"
	"log"

	"github.com/mohidex/data-pipeline/config"
	"github.com/mohidex/data-pipeline/loader"
	"github.com/mohidex/data-pipeline/reader"
	"github.com/mohidex/data-pipeline/storage"
)

func main() {
	conf := config.LoadConfig()
	// Create a new PubSubMessageReader client.
	messageReader, err := reader.NewPubSubMessageReader(conf.ProjectID, conf.SubscriptionID, conf.CredentialsFile)
	if err != nil {
		log.Fatalf("Error creating PubSubMessageReader: %v", err)
	}

	dataStoreclient, err := storage.NewDatastoreClient(conf.ProjectID, conf.CredentialsFile)
	if err != nil {
		log.Fatalf("Error initializing Datastore client: %v", err)
	}

	loader := &loader.Loader{
		PubSubReader:   messageReader,
		Storage:        dataStoreclient,
		WorkerPoolSize: conf.WorkerPoolSize,
	}
	fmt.Println("Start Loader")
	loader.Load()
	fmt.Println("End Loader")
}
