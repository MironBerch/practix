package utils

import (
	"github.com/ua-parser/uap-go/uaparser"
)

func GetDeviceType(uagent string) string {
	parser := uaparser.NewFromSaved()
	client := parser.Parse(uagent)
	return client.Os.Family
}
