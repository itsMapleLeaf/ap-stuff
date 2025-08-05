create WORLD:
	git subtree add --prefix worlds/{{WORLD}} template main

update WORLD:
	git stash
	git subtree pull --prefix worlds/{{WORLD}} template main
	git stash pop

update-all: (update "distance")  (update "sdvx")

[working-directory: 'worlds']
build WORLD:
	PYTHONPATH="../archipelago" uv run -m {{WORLD}}.scripts.build

build-all: (build "distance")  (build "sdvx")

[working-directory: 'worlds']
fetch-sdvx-songs:
	PYTHONPATH="../archipelago" uv run -m sdvx.scripts.fetch_songs
