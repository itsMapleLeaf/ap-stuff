export PYTHONPATH := justfile_directory() / "archipelago"

build-all: (build "distance")  (build "sdvx")

[working-directory: 'worlds']
build WORLD:
	uv run -m {{WORLD}}.scripts.build

update-all: (update "distance")  (update "sdvx")

update WORLD:
	git stash
	git subtree pull --prefix worlds/{{WORLD}} template main
	git stash pop

create WORLD:
	git subtree add --prefix worlds/{{WORLD}} template main

play:
	uv run -m scripts.play

[working-directory: 'worlds']
fetch-sdvx-songs:
	uv run -m sdvx.scripts.fetch_songs
