export PYTHONPATH := justfile_directory() / "archipelago"

build *worlds:
    uv run -m scripts.build {{ worlds }}

update-all: (update "distance") (update "sdvx")

update WORLD:
    git stash
    git subtree pull --prefix worlds/{{ WORLD }} template main
    git stash pop

create WORLD:
    git subtree add --prefix worlds/{{ WORLD }} template main

export:
    uv run -m scripts.export

[working-directory('worlds')]
fetch-sdvx-songs:
    uv run -m sdvx.scripts.fetch_songs
