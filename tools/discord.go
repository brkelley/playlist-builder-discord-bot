package tools

import (
	"fmt"
	"log"
	"os"

	"github.com/bwmarrin/discordgo"
)

func InitDiscordBot() {
	discord_token := os.Getenv("DISCORD_TOKEN")
	discordgo, err := discordgo.New("Bot " + discord_token)
	if err != nil {
		log.Fatalf("error creating Discord session: %v\n", err)
		return
	}

	discordgo.AddHandler(messageCreate)
	err = discordgo.Open()
	if err != nil {
		log.Fatalf("error opening connection: %v\n", err)
		return
	}

	fmt.Printf("LimeBot is listening\n")
}

func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {

	// Ignore all messages created by the bot itself
	// This isn't required in this specific example but it's a good practice.
	if m.Author.ID == s.State.User.ID {
		return
	}

	// if strings.Contains(m.Content, "!add") {
	// 	fmt.Println("you wanna add a song huh")
	// }

	InitSpotify()

	_, _ = s.ChannelMessageSendReply(m.ChannelID, "pong", m.Reference())
}
