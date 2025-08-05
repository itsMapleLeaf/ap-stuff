build-all: (build "distance")  (build "sdvx")

[working-directory: 'worlds']
build WORLD:
	PYTHONPATH="../archipelago" uv run -m {{WORLD}}.scripts.build


update-all: (update "distance")  (update "sdvx")

update WORLD:
	git stash
	git subtree pull --prefix worlds/{{WORLD}} template main
	git stash pop


create WORLD:
	git subtree add --prefix worlds/{{WORLD}} template main

[working-directory: 'worlds']
fetch-sdvx-songs:
	PYTHONPATH="../archipelago" uv run -m sdvx.scripts.fetch_songs
