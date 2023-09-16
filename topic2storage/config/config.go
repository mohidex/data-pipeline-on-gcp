package config

import "os"

type Config struct {
	ProjectID       string
	SubscriptionID  string
	CredentialsFile string
	WorkerPoolSize  string
}

func LoadConfig() *Config {
	return &Config{
		ProjectID:       getEnv("GCP_PROJECT_ID", "gcp-project-id"),
		SubscriptionID:  getEnv("TOPIC_SUB_ID", "pub-sub-topic-subcriber"),
		CredentialsFile: getEnv("CREDENTIALS_PATH", "service-account-client-secret.json"),
		WorkerPoolSize:  getEnv("POOL_SIZE", "3"),
	}
}

// getEnv returns the value of an environment variable or a default value if not set.
func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
