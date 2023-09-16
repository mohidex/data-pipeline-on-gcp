package types

import (
	"reflect"
	"time"
)

type Product struct {
	ID     string    `json:"id"`
	Key    string    `json:"key"`
	Name   string    `json:"name"`
	Price  float32   `json:"price"`
	Source string    `json:"source"`
	Date   time.Time `json:"date"`
}

func isDefaultTime(t time.Time) bool {
	return t.Equal(time.Time{})
}

func (p *Product) IsValid() bool {
	v := reflect.ValueOf(p).Elem()

	// Make sure obj is a struct
	if v.Kind() != reflect.Struct {
		return false
	}

	// Check each field of the struct
	for i := 0; i < v.NumField(); i++ {
		fieldValue := v.Field(i)
		fieldType := v.Type().Field(i)

		// Check if the field type is time.Time
		if fieldType.Type == reflect.TypeOf(time.Time{}) {
			if isDefaultTime(fieldValue.Interface().(time.Time)) {
				return false
			}
		}
	}

	return true
}
