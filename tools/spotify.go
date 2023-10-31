package tools

import (
	"context"
	"log"
	"os"

	"github.com/zmb3/spotify"
	"golang.org/x/oauth2/clientcredentials"
)

var Client spotify.Client
var CurrentUser *spotify.PrivateUser
var redirectURL = "localhost:8080"

func InitSpotify() {
	// Authenticate
	authConfig := &clientcredentials.Config{
		ClientID:     os.Getenv("SPOTIFY_CLIENT_ID"), // client ID from Spotify developer dashboard
		ClientSecret: os.Getenv("SPOTIFY_SECRET"),    // client secret from Spotify developer dashboard
		TokenURL:     spotify.TokenURL,
	}
	//a := spotify.NewAuthenticator(redirectURL, spotify.ScopePlaylistModifyPublic)

	accessToken, err := authConfig.Token(context.Background())
	if err != nil {
		log.Fatalf("Error authenticating with Spotify: %v\n", err)
	}
	Client := spotify.Authenticator{}.NewClient(accessToken)

	// Populate current user
	CurrentUser, err = Client.CurrentUser()
	if err != nil {
		log.Fatalf("Error getting current user: %v\n", err)
	}

	// Check if playlist exists, and make it if not
	playlistID := Config.PlaylistId

	if playlistID == "" {
		Client.CreateCollaborativePlaylistForUser(CurrentUser.ID, "The Sound of Citrus", "Automatically generated playlist from LimeBot")
	}

	// playlist, err := Client.GetPlaylist(playlistID)
}
