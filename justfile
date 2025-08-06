games_dir := justfile_directory() / "games"
dist_dir := justfile_directory() / "dist"
generate_output_dir := dist_dir / "generate"

user_archipelago_dir := 'C:/ProgramData/Archipelago'
archipelago_generate := user_archipelago_dir / "ArchipelagoGenerate.exe"
archipelago_server := user_archipelago_dir / "ArchipelagoServer.exe"

export PYTHONPATH := justfile_directory() / "archipelago"

build *worlds:
    uv run -m scripts.build {{ worlds }}

generate game:
    rm -rf "{{ generate_output_dir }}"
    mkdir -p "{{ generate_output_dir }}"

    {{ archipelago_generate }} \
        --player_files_path "{{ games_dir / game }}" \
        --outputpath "{{ generate_output_dir }}"

    cd "{{ generate_output_dir }}"; unzip AP_*.zip

play game="local": build (generate game)
    cd "{{ generate_output_dir }}"; {{ archipelago_server }} *.archipelago

export game:
    uv run -m scripts.export {{ game }}

update-all: (update "distance") (update "sdvx")

update WORLD:
    git stash
    git subtree pull --prefix worlds/{{ WORLD }} template main
    git stash pop

create WORLD:
    git subtree add --prefix worlds/{{ WORLD }} template main

[working-directory('worlds')]
fetch-sdvx-songs:
    uv run -m sdvx.scripts.fetch_songs
