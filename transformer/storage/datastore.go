package storage

import (
	"context"
	"fmt"

	"cloud.google.com/go/datastore"
	"github.com/mohidex/data-pipeline/types"
	"google.golang.org/api/option"
)

// DatastoreClient represents the Datastore client.
type DatastoreClient struct {
	client *datastore.Client
}

// NewDatastoreClient creates a new DatastoreClient with the given project ID and credentials file path.
func NewDatastoreClient(projectID, credentialsFile string) (*DatastoreClient, error) {
	ctx := context.Background()
	client, err := datastore.NewClient(ctx, projectID, option.WithCredentialsFile(credentialsFile))
	if err != nil {
		return nil, fmt.Errorf("failed to initialize Datastore client: %v", err)
	}
	return &DatastoreClient{
		client: client,
	}, nil
}

// SaveProduct saves the product data to Google Cloud Datastore.
func (dc *DatastoreClient) SaveProduct(ctx context.Context, product types.Product) error {
	key := datastore.NameKey("Product", product.ID, nil)

	if _, err := dc.client.Put(ctx, key, &product); err != nil {
		return fmt.Errorf("failed to save product to Datastore: %v", err)
	}

	fmt.Println("Product saved successfully!")
	return nil
}

// GetProduct retrieves a product from Google Cloud Datastore by its ID.
func (dc *DatastoreClient) GetProduct(ctx context.Context, productID string) (*types.Product, error) {
	key := datastore.NameKey("Product", productID, nil)
	product := new(types.Product)

	if err := dc.client.Get(ctx, key, product); err != nil {
		return nil, fmt.Errorf("failed to retrieve product from Datastore: %v", err)
	}

	return product, nil
}

// DeleteProduct deletes a product from Google Cloud Datastore by its ID.
func (dc *DatastoreClient) DeleteProduct(ctx context.Context, productID string) error {
	key := datastore.NameKey("Product", productID, nil)

	if err := dc.client.Delete(ctx, key); err != nil {
		return fmt.Errorf("failed to delete product from Datastore: %v", err)
	}

	fmt.Println("Product deleted successfully!")
	return nil
}
