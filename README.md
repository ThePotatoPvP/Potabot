# 🥔 PotaBot 🥔

PotaBot is a general purpose Discord bot made specifically for a private server. This bot has a potato theme and comes equipped with a helpful help page and all the basic music commands you need to get the party started.

## Commands

- General
    - `/ping` : Sends Pong.
    - `/8b` : Helps you make tough decisions.
    - `/roast` : Roasts someone for you.
    - `/luv` : Sends a pickup line aimed to your loved one.
- Music
    - `p!play <song>` : Plays audio from a link.
    - `p!skip` : Skips the currently playing song.
    - `p!queue` : Displays the current song queue.
    - `p!stop` : Stops playing music and clears the queue.
- Miscellianous
    - `/bubble` : Adds a speech bubble on top of an image and turns it into a GIF.
    - `/yt-summarise` : Gives a brief summary  of a youtube video

## Contributing

If you're interested in contributing to Potato Bot, feel free to fork the repository and submit a pull request. The code is open source and available here.

## Installation

To run PotaBot on your own server, follow these steps:

1. Clone the repository or download the zip file.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a `.token` file and put your Discord bot token in it.
4. Run `python main.py` to start the bot.

## Events

This bot was also made to allow for easy creation of custom events, for now the only that is implemented properly is `ScheduledEvents` which are events that happen based on a schedule. By default the events will happen every day at midnight but you're able to change the time, to set a special day of the week or even of the month. The following example will send a message to a given channel every monday at 7pm.

```python
@ScheduledEvent(hour=19, minute=0, day_of_week=0)
async def foo(client: discord.Client):
    channel = client.get_channel('channel-id')
    await channel.send('foo')
```

To allow for simple usage, all of those events shall be typed the same as this example and be in [`ScheduledEvents`](src/Events/ScheduledEvents.py)

## License

PotaBot is licensed under the GNU General Public License v3.0. See LICENSE for more information.
