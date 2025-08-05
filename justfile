create WORLD:
	git subtree add --prefix worlds/{{WORLD}} template main

update WORLD:
	git subtree pull --prefix worlds/{{WORLD}} template main

[working-directory: 'worlds']
build WORLD:
	PYTHONPATH="../archipelago" uv run -m {{WORLD}}.scripts.build

[working-directory: 'worlds']
fetch-sdvx-songs:
	PYTHONPATH="../archipelago" uv run -m sdvx.scripts.fetch_songs
