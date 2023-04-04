# Droombot as a container

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
