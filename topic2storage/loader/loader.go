package loader

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"strconv"
	"time"

	"cloud.google.com/go/pubsub"
	"github.com/mohidex/data-pipeline/reader"
	"github.com/mohidex/data-pipeline/storage"
	"github.com/mohidex/data-pipeline/types"
)

type Loader struct {
	PubSubReader   reader.MessageReader
	Storage        storage.StorageWriter
	WorkerPoolSize string
}

func (l *Loader) Load() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	// Create a channel for pubsub Message
	msgChan := make(chan *pubsub.Message, 100)

	go func() {
		// Receive a message from the subscription.
		err := l.PubSubReader.PullMessage(ctx, func(msg *pubsub.Message) {
			msgChan <- msg
		})

		if err != nil {
			log.Printf("Error pulling message: %v", err)
		}
	}()

	select {
	case <-ctx.Done():
		// Close msgChan channel since timeout context is triggered.
		close(msgChan)
	default:

		poolSize, _ := strconv.Atoi(l.WorkerPoolSize)
		// Start workers pool to store product to database
		for sWorker := 1; sWorker <= poolSize; sWorker++ {
			ctx := context.Background()
			go l.storeProductWorker(ctx, msgChan)
		}

	}
	<-ctx.Done()
}

// processMessage process a single pubsub message and parse it into a product type.
func processMessage(msg *pubsub.Message) *types.Product {
	var product types.Product
	if err := json.Unmarshal([]byte(string(msg.Data)), &product); err != nil {
		fmt.Println("Error parsing JSON:", err)
		return &types.Product{}
	}
	return &product
}

// storeProductWorker store the product struct if it is valid and send Ack signal to pub/sub.
func (l *Loader) storeProductWorker(ctx context.Context, msgChan <-chan *pubsub.Message) {
	for msg := range msgChan {
		product := processMessage(msg)
		if !product.IsValid() {
			fmt.Println("The Product is not valid.")
			return
		}
		if err := l.Storage.SaveProduct(ctx, *product); err != nil {
			log.Fatalf("Error saving product: %v\n", err)
		}
		// Acknowledge the message to remove it from the subscription.
		l.PubSubReader.AcknowledgeMessage(context.Background(), msg)

	}
}
