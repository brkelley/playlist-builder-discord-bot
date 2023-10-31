package tools

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
)

var json_filename = "bot_config.json"
var Config BotConfig

type BotConfig struct {
	PlaylistId string `json:"playlistId"`
}

func ReadBotConfig() {
	jsonFile, err := os.Open(json_filename)
	if err != nil {
		log.Fatalf("error reading config: %v\n", err)
	}
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)
	json.Unmarshal(byteValue, &Config)
}
