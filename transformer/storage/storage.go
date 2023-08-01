package storage

import (
	"context"

	"github.com/mohidex/data-pipeline/types"
)

type StorageWriter interface {
	SaveProduct(ctx context.Context, product types.Product) error
	GetProduct(ctx context.Context, productID string) (*types.Product, error)
	DeleteProduct(ctx context.Context, productID string) error
}
