package main

import (
	"limebot/tools"
	"log"

	"github.com/joho/godotenv"
)

func main() {
	// Load env variables
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	// Load in our database (heh)
	tools.ReadBotConfig()

	// Run Discord bot
	tools.InitDiscordBot()

	// Run web server
	tools.InitWebServer()
}
