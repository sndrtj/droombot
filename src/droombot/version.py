import importlib.metadata
import subprocess


def get_version() -> str:
    """Get the current version of droombot.

    This will be of shape <x.y.z>-<git short hash>. The git hash can only
    be computed if we are in a git repo and git is installed.
    So from docker or from pip installs, the hash will be empty. Lastly, if we are in
    a git repo, we will append a `-dirty` tag if the current checkout is in a dirty
    state.

    :return: Version string
    """
    try:
        git_tag: str | None = (
            subprocess.run(
                ["git", "describe", "--always", "--dirty"],
                capture_output=True,
                check=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_tag = None

    base_version = importlib.metadata.version("droombot")

    if git_tag is None:
        return base_version

    return f"{base_version}-{git_tag}"


VERSION = get_version()
