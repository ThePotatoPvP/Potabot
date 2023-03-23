# 🥔 PotaBot 🥔

PotaBot is a general purpose Discord bot made specifically for a private server. This bot has a potato theme and comes equipped with a helpful help page and all the basic music commands you need to get the party started.

## Commands

- `p!help`: Displays a helpful help page with all available commands.
- `p!play <song>`: Plays audio from a link.
- `p!skip`: Skips the currently playing song.
- `p!queue`: Displays the current song queue.
- `p!stop`: Stops playing music and clears the queue.

## Contributing

If you're interested in contributing to Potato Bot, feel free to fork the repository and submit a pull request. The code is open source and available here.

## Installation

To run PotaBot on your own server, follow these steps:

1. Clone the repository or download the zip file.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a `.token` file and put your Discord bot token in it.
4. Run `python main.py` to start the bot.

## Advanced

PotaBot has a unique playlist feature that allows anyone to suggest a song by sending a link or audio file to the bot in a DM. The bot will then download the audio file and store it in the `Musica/` directory. However, moderators of the server have to review the proposed songs before they can be added to the playlist.

To review the proposed songs, use the following commands:

- `p!review`: Plays the next unreviewed songs. Moderators can use this command to listen to the proposed songs and decide if they should be added to the playlist or not.
- `p!remove`: Removes the current song being reviewed from the `directory. Moderators can use this command to reject a proposed song.
- `p!rename <name>`: Renames the current song being reviewed to the specified name. Moderators can use this command to make it easier to find the proposed song later.

To listen to the playlist, use the `p!play <song>` command with or without a query. If no argument is provided, the bot will play the default playlist by default.

Note that the playlist feature requires disk space to store the downloaded audio files. Make sure you have enough space before using this feature. Also, since this directly uses the architecture of your file system, you may face issues that I didn't plan, please contact me if you need help with setting that up. 
Also you might want to change the `update_annonce` function in `src/Music/MusicFunctions` to fit your server.

## License

PotaBot is licensed under the GNU General Public License v3.0. See LICENSE for more information.
