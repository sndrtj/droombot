# Droombot

Droombot is a discord bot for generating images from text prompts.

At current, it uses an API call to Stability.ai to generate images.
A future version may support running Stable Diffusion directly.


https://user-images.githubusercontent.com/7782240/229916443-2cc0aa4d-188b-47c1-947e-9fd1708f4fba.mp4


## Installing

:zap: Note: this step is not necessary if using a Container (see below)

Run the following, preferably in a virtual environment, to install droombot

```console
pip install droombot
```

## How to run

:zap: Note: this step is not necessary if using a Container (see below)

Configure your environment (see configuration options below), and make sure a
redis instance is running on your network (we recommend using a container).

To start the bot, run the following in the virtual environment:

```console
droombot server
```

To start a worker, run the following in the virtual environment

```console
droombot worker
```

## How to use in discord

Use the `/prompt` command to type your prompt. This by default uses whatever model
Stability AI now considers its "core". You can also select Stable Diffusion 3 and
Stable Diffusion 3 Turbo models by appending `-m sd3` or `-m sd3-turbo` to your
prompt.

You can give individual words in your prompt more some weight by doing something like
the following;
``A table with (red:0.5) raspberries and (purple:0.5) blueberries.``

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


## Container

Droombot can run as a container. For a howto using Docker or Podman, see the
[container docs](docs/containers.md).

## Future plans

1. Expose additional options, such as multiple images and model selection.
2. Ability to run Stable Diffusion directly, with a separate worker class
3. Prompt translations, allowing users to use prompts in their own language.
