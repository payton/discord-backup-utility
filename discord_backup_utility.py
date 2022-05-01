import json

import os
import shutil

import click
import requests
import logging
import time

_logger = logging.getLogger(name="discord-backup-utility")
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://discord.com/api/v9"


@click.group()
@click.option('-o', '--output', default="./backup", show_default=True, type=str, help="directory to write backup to")
@click.option('-t', '--token', required=True, type=str, help="authorization token from science endpoint")
@click.option('-s', '--server-id', required=True, type=str, help="ID of server to backup data from")
@click.pass_context
def cli(ctx, output, token, server_id):
    ctx.ensure_object(dict)

    if not os.path.exists(output):
        _logger.info(f"Creating directory for Discord backup at '{output}'")
        os.mkdir(output)
    else:
        _logger.error(f"Directory '{output}' already exists. Please remove it and run command again.")
        raise Exception(f"Directory '{output}' already exists. Please remove it and run command again.")

    ctx.obj['OUTPUT'] = output
    ctx.obj['TOKEN'] = token
    ctx.obj['SERVER_ID'] = server_id

    # Get server metadata
    response = requests.get(
        f"{BASE_URL}/guilds/{ctx.obj['SERVER_ID']}",
        headers={
            "Authorization": ctx.obj['TOKEN']
        }
    )
    ctx.obj['SERVER_METADATA'] = response.json()

    # Write server metadata
    server_metadata = f"{output}/metadata.json"
    _logger.info(f"Writing server metadata to: {server_metadata}")
    with open(server_metadata, 'w') as f:
        json.dump(ctx.obj["SERVER_METADATA"], f, indent=4)


@cli.command()
@click.pass_context
def save_server(ctx):
    """Saves entire server."""
    _logger.info("Backing up entire server")
    ctx.invoke(save_channels)
    ctx.invoke(save_roles)
    ctx.invoke(save_emojis)
    ctx.invoke(save_stickers)


@cli.command()
@click.option(
    '-c', '--channel', 'requested_channels',
    required=False, multiple=True, type=str, help="IDs of channels to save"
)
@click.pass_context
def save_channels(ctx, requested_channels):
    """Saves all messages from specified channel IDs. If no channel IDs are passed in, we save the entire server."""
    # Get all channels for given server ID
    response = requests.get(
        f"{BASE_URL}/guilds/{ctx.obj['SERVER_ID']}/channels",
        headers={
            "Authorization": ctx.obj['TOKEN']
        }
    )
    server_channels = response.json()

    channels_directory = f"{ctx.obj['OUTPUT']}/channels"
    os.mkdir(channels_directory)

    # Iterate over all channels filtered by input (if present... else all channels)
    for channel in [c for c in server_channels if c["id"] in requested_channels or len(requested_channels) == 0]:
        _logger.info(f"Processing channel: {channel['name']}")

        # Create subdirectory for channel
        working_directory = f"{channels_directory}/{channel['name']}"
        os.mkdir(working_directory)

        # Get first batch of messages
        response = requests.get(
            f"{BASE_URL}/channels/{channel.get('id', None)}/messages?limit=100",
            headers={
                "Authorization": ctx.obj['TOKEN']
            }
        )
        while len(response.json()) > 0 and response.status_code == 200:
            message_file = f"{working_directory}/{response.json()[-1]['id']}.json"
            _logger.info(f"Writing batch of messages to: {message_file}")
            with open(message_file, 'w') as f:
                json.dump(response.json(), f, indent=4)
                response = requests.get(
                    f"{BASE_URL}/channels/{channel.get('id', None)}/messages?limit=100&before={response.json()[-1]['id']}",
                    headers={
                        "Authorization": ctx.obj['TOKEN']
                    }
                )
                time.sleep(1)


@cli.command()
@click.pass_context
def save_emojis(ctx):
    """Saves all emojis from server."""
    # Create directory for emojis
    emojis_directory = f"{ctx.obj['OUTPUT']}/emojis"
    _logger.info(f"Creating directory for emojis at '{emojis_directory}'")
    os.mkdir(emojis_directory)

    # Write emoji metadata
    emoji_metadata = f"{emojis_directory}/metadata.json"
    _logger.info(f"Writing emoji metadata to: {emoji_metadata}")
    with open(emoji_metadata, 'w') as f:
        json.dump(ctx.obj["SERVER_METADATA"]["emojis"], f, indent=4)

    # Save each emoji file
    for emoji in ctx.obj["SERVER_METADATA"]["emojis"]:
        emoji_file = f"{emojis_directory}/{emoji['name']}.png"
        _logger.info(f"Writing emoji to: {emoji_file}")

        response = requests.get(f"https://cdn.discordapp.com/emojis/{emoji['id']}", stream=True)
        with open(emoji_file, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


@cli.command()
@click.pass_context
def save_roles(ctx):
    """Saves all roles from server."""
    # Create directory for emojis
    roles_directory = f"{ctx.obj['OUTPUT']}/roles"
    _logger.info(f"Creating directory for roles at '{roles_directory}'")
    os.mkdir(roles_directory)

    # Write emoji metadata
    roles_metadata = f"{roles_directory}/metadata.json"
    _logger.info(f"Writing emoji metadata to: {roles_metadata}")
    with open(roles_metadata, 'w') as f:
        json.dump(ctx.obj["SERVER_METADATA"]["roles"], f, indent=4)

    # Save each emoji file
    for role in ctx.obj["SERVER_METADATA"]["roles"]:
        role_file = f"{roles_directory}/{role['name']}.webp"
        _logger.info(f"Writing role icon to: {role_file}")

        response = requests.get(f"https://cdn.discordapp.com/role-icons/{ctx.obj['SERVER_ID']}/{role['icon']}.webp?size=512&quailty=lossless", stream=True)
        with open(role_file, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


@cli.command()
@click.pass_context
def save_stickers(ctx):
    """Saves all stickers from server."""
    # Create directory for emojis
    stickers_directory = f"{ctx.obj['OUTPUT']}/stickers"
    _logger.info(f"Creating directory for stickers at '{stickers_directory}'")
    os.mkdir(stickers_directory)

    # Write emoji metadata
    stickers_metadata = f"{stickers_directory}/metadata.json"
    _logger.info(f"Writing sticker metadata to: {stickers_metadata}")
    with open(stickers_metadata, 'w') as f:
        json.dump(ctx.obj["SERVER_METADATA"]["stickers"], f, indent=4)

    # Save each emoji file
    for sticker in ctx.obj["SERVER_METADATA"]["stickers"]:
        sticker_file = f"{stickers_directory}/{sticker['name']}.webp"
        _logger.info(f"Writing sticker to: {sticker_file}")

        response = requests.get(f"https://media.discordapp.net/stickers/{sticker['id']}.webp?size=640", stream=True)
        with open(sticker_file, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


if __name__ == '__main__':
    cli(obj={})
