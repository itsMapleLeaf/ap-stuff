games_dir := justfile_directory() / "games"
dist_dir := justfile_directory() / "dist"
generate_output_dir := dist_dir / "generate"

user_archipelago_dir := 'C:/ProgramData/Archipelago'
archipelago_generate := user_archipelago_dir / "ArchipelagoGenerate.exe"
archipelago_server := user_archipelago_dir / "ArchipelagoServer.exe"

export PYTHONPATH := justfile_directory() / "archipelago"

# build all manual worlds into your Archipelago custom_worlds folder
build *worlds:
    uv run -m scripts.build {{ worlds }}

# generate and serve a multiworld for a given game
play game="local": (generate game) serve

# generate a multiworld with a given game
generate game: build
    rm -rf "{{ generate_output_dir }}"
    mkdir -p "{{ generate_output_dir }}"

    {{ archipelago_generate }} \
        --player_files_path "{{ games_dir / game }}" \
        --outputpath "{{ generate_output_dir }}"

    cd "{{ generate_output_dir }}"; unzip AP_*.zip

# serve a generated multiworld
serve:
    cd "{{ generate_output_dir }}"; {{ archipelago_server }} *.archipelago

# create apworlds and a stitched config for a multi
export game:
    uv run -m scripts.export {{ game }}

# update all manual worlds with the latest template code
update-all: (update "distance") (update "sdvx")

# update a given manual world with the latest template code
update WORLD:
    git stash
    git subtree pull --prefix worlds/{{ WORLD }} template main
    git stash pop

# create a new manual world
create WORLD:
    git subtree add --prefix worlds/{{ WORLD }} template main

# update songs for the sound voltex manual
[working-directory('worlds')]
fetch-sdvx-songs:
    uv run -m sdvx.scripts.fetch_songs
