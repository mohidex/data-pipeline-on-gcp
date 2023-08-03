package reader

import (
	"context"
	"fmt"

	"cloud.google.com/go/pubsub"
	"google.golang.org/api/option"
)

type PubSubMessageReader struct {
	client       *pubsub.Client
	subscription *pubsub.Subscription
}

// NewPubSubMessageReader creates a new PubSubMessageReader.
func NewPubSubMessageReader(projectID, subscriptionID, credentialsFile string) (*PubSubMessageReader, error) {
	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, projectID, option.WithCredentialsFile(credentialsFile))
	if err != nil {
		return nil, fmt.Errorf("failed to create Pub/Sub client: %v", err)
	}

	subscription := client.Subscription(subscriptionID)
	return &PubSubMessageReader{
		client:       client,
		subscription: subscription,
	}, nil
}

// PullMessage pulls messages from the Pub/Sub subscription and invokes the handler function for each message.
func (r *PubSubMessageReader) PullMessage(ctx context.Context, handler func(*pubsub.Message)) error {
	err := r.subscription.Receive(ctx, func(ctx context.Context, msg *pubsub.Message) {
		handler(msg)
	})

	return err
}

// AcknowledgeMessage acknowledges a message to remove it from the subscription.
func (r *PubSubMessageReader) AcknowledgeMessage(ctx context.Context, msg *pubsub.Message) {
	msg.Ack()
}
