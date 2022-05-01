# Discord Backup Utility

A simple command line interface to backup data from a Discord server. This is meant to be used as a worst-case resort in the event that a Discord server is compromised.

## Requirements
Before using the CLI, you must obtain your authorization token.

DO NOT SHARE THIS TOKEN WITH ANYONE. THIS IS THE EQUIVALENT OF YOUR DISCORD PASSWORD.

1. Open your browser and navigate to Discord
2. Open web developer tools and go to the `Network` panel
3. Refresh the page
4. Search your requests for one named `science`
5. Click on one of the `science` requests and go to Headers
6. Copy the value of the `Authorization` request header

AGAIN, DO NOT SHARE THIS VALUE WITH ANYONE UNDER ANY CIRCUMSTANCE.

## Usage

After cloning the repository, install dependencies

`pip install -r requirements.txt`

View available commands with `python3 discord_backup_utility.py`

```bash
Usage: discord_backup_utility.py [OPTIONS] COMMAND [ARGS]...

Options:
  -o, --output TEXT     directory to write backup to  [default: ./backup]
  -t, --token TEXT      authorization token from science endpoint  [required]
  -s, --server-id TEXT  ID of server to backup data from  [required]
  --help                Show this message and exit.

Commands:
  save-channels  Saves all messages from specified channel IDs.
  save-emojis    Saves all emojis from server.
  save-roles     Saves all roles from server.
  save-server    Saves entire server.
  save-stickers  Saves all stickers from server.
```

There are two required options: token and server ID.

Server ID can be obtains from any Discord URL in the server you want to run a backup for. For example, let's take a look at this URL from the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39):

`https://discord.com/channels/968297868257550346/968305408345251892`

In this case, the first number (`968297868257550346`) after `channels` is the server ID and the second number (`968305408345251892`) is the channel ID of the channel I am presently on (open discussion).

The token can be obtained by following the requirements section. AGAIN, DO NOT SHARE THIS VALUE WITH ANYONE UNDER ANY CIRCUMSTANCE.

Optionally, you can specify a directory with the output option. This is where the backup data will be written. By default, this is done in a `backup` directory.

## Examples

Now that you have your server ID and token (DO NOT SHARE THIS VALUE WITH ANYONE UNDER ANY CIRCUMSTANCE), you can run one of our commands.

To backup emojis for the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39), we would run

```
python3 discord_backup_utility.py -t MY_TOP_SECRET_TOKEN -s 968297868257550346 save-emojis
```

To backup emojis for the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39) in a folder named "my-backup", we would run

```
python3 discord_backup_utility.py -o ./my-backup -t MY_TOP_SECRET_TOKEN -s 968297868257550346 save-emojis
```

To backup messages in the open-discussion channel for the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39), we would run

```
python3 discord_backup_utility.py -t MY_TOP_SECRET_TOKEN -s 968297868257550346 save-channels -c 968305408345251892
```

To backup all messages in the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39), we would run

```
python3 discord_backup_utility.py -t MY_TOP_SECRET_TOKEN -s 968297868257550346 save-channels
```

Finally, to backup all known data for the [Crypto Baristas Discord](https://discord.gg/ddbjAYYh39), we would run:

```
python3 discord_backup_utility.py -t MY_TOP_SECRET_TOKEN -s 968297868257550346 save-server
```

