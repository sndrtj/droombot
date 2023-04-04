# Droombot

Droombot is a discord bot for generating images from text prompts.

At current, it uses an API call to Stability.ai to generate images.
A future version may support running Stable Diffusion directly.

## Installing

:zap: Note: this step is not necessary if using a Container (see below)

Install [poetry](https://python-poetry.org/) if you haven't already.
Then run the following where-ever you cloned this repo.

```console
poetry install
```

## How to run

:zap: Note: this step is not necessary if using a Container (see below)

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


## Container

We recommend running droombot as a container. The provided Dockerfile builds a
container that can run both the `server` and `worker` components.


### Docker
When using docker, run the following:

```console
docker build . -t droombot
docker run -p 6379:6379 -d --name droombot-redis redis:latest
docker run -e DISCORD_BOT_TOKEN=<token> -e DISCORD_GUILD_IDS=<ids> -d --name droombot-server droombot server
docker run -e STABILITY_API_KEY=<key> -e DISCORD_BOT_TOKEN=<token> -e DISCORD_GUILD_IDS=<ids> -d --name droombot-worker droombot worker
```

### Podman

When using podman, you can create a podman pod. After setting up the services
within the pod, you can then generate a set of systemd unit files. Very useful for
automatically starting services at boot!

```console
podman build . -t droombot
podman pod create --name droombot-pod
podman run -d --name droombot-redis --pod droombot-pod redis:latest
podman run -e DISCORD_BOT_TOKEN=<token> -e DISCORD_GUILD_IDS=<ids> -d --name droombot-server --pod droombot-pod  droombot server
podman run -e STABILITY_API_KEY=<key> -e DISCORD_BOT_TOKEN=<token> -e DISCORD_GUILD_IDS=<ids> -d --name droombot-worker --pod droombot-pod droombot worker
```

You can then run `podman generate systemd --new --files --name droombot-pod` to
generate systemd unit files. See [this guide](https://www.redhat.com/sysadmin/podman-run-pods-systemd-services)
for how to configure systemd with the generated units.


## Future plans

1. Publish to PyPI
2. Expose additional options, such as multiple images and model selection.
3. Ability to run Stable Diffusion directly, with a separate worker class
4. Prompt translations, allowing users to use prompts in their own language.
