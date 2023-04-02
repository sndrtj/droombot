# Droombot

Droombot is a discord bot for generating images from text prompts.

At current, it uses an API call to Stability.ai to generate images.
A future version may support running Stable Diffusion directly.

## Installing

Install [poetry](https://python-poetry.org/) if you haven't already.
Then run the following where-ever you cloned this repo.

```console
poetry install
```

## How to run

Configure your environment (see configuration options below), and make sure a
redis instance is running on your network (we recommend using a container).

To start the bot, run the following where-ever you cloned this repo.

```console
poetry run droombot server
```

To start a worker, run the following where-ever you cloned this repo.

```console
poetry run droombot worker
```

## Components

Droombot consists of two components:

1. The `server`, this handles interaction with the user. I.e., it handles incoming
   prompts and replies. It provides the Discord bot users interact with.
2. One or more `worker`s. These handle the actual image generation.

Redis is used as a message broker between the `server` and the `worker`(s).

## Configuration

All configuration is handled via environment variables. See the following table

| Environment variable      | Description                                                                    | Is Required               |
|---------------------------|--------------------------------------------------------------------------------|---------------------------|
| `DISCORD_BOT_TOKEN`       | Token for your discord application                                             | Yes                       |
| `DISCORD_GUILD_IDS`       | Comma-separated list of guild (server) ids you want to allow access to the bot | Yes                       |
| `STABILITY_API_KEY`       | API key from Stability AI                                                      | Yes                       |
| `REDIS_HOST`              | Hostname of Redis instance                                                     | No, defaults to localhost |
| `REDIS_PORT`              | Port of Redis instance                                                         | No, defaults to 6379      |
| `REDIS_KEY_LIFETIME`      | Number of seconds for keys to expire                                           | No, defaults to 300       |
| `MAX_REQUESTS_PER_MINUTE` | Maximum number of requests per minute to any remote services                   | No, defaults to 100       |

## Todo:

* Dockerfile / Podmanfile
    * Instructions on how to use systemd to autostart


## Future plans

1. Expose additional options, such as multiple images and model selection.
2. Ability to run Stable Diffusion directly, with a separate worker class
3. Prompt translations, allowing users to use prompts in their own language.
