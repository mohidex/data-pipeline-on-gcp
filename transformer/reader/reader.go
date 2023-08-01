package reader

import (
	"context"

	"cloud.google.com/go/pubsub"
)

type MessageReader interface {
	PullMessage(ctx context.Context, handler func(*pubsub.Message)) error
	AcknowledgeMessage(ctx context.Context, msg *pubsub.Message)
}
