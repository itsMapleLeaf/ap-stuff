worlds_dirname := "manual_worlds"

games_dir := justfile_directory() / "games"
dist_dir := justfile_directory() / "dist"
generate_dir := dist_dir / "generate"
generate_players_dir := dist_dir / "generate/players"
generate_output_dir := dist_dir / "generate/output"

user_archipelago_dir := 'C:/ProgramData/Archipelago'
archipelago_generate := user_archipelago_dir / "ArchipelagoGenerate.exe"
archipelago_server := user_archipelago_dir / "ArchipelagoServer.exe"

export PYTHONPATH := justfile_directory() / "archipelago"

# build all manual worlds into your Archipelago custom_worlds folder
build *worlds:
    uv run -m scripts.build {{ worlds }}

# generate and serve a multiworld for a given game
play game: (generate game) serve

# generate a multiworld with a given game
generate game: build
    rm -rf "{{ generate_dir }}"
    mkdir -p "{{ generate_players_dir }}"
    mkdir -p "{{ generate_output_dir }}"

    uv run -m scripts.create_generate_players_dir "{{ game }}"

    uv run -m archipelago.Generate \
        --player_files_path "{{ generate_players_dir }}" \
        --outputpath "{{ generate_output_dir }}"

    cd "{{ generate_output_dir }}"; unzip AP_*.zip

# serve a generated multiworld
serve:
    cd "{{ generate_output_dir }}"; {{ archipelago_server }} *.archipelago

# create apworlds and a stitched config for a multi
export game:
    uv run -m scripts.export {{ game }}

# create a new manual world
create world:
    cp -r template/src manual_worlds/{{ world }}

# print the data for a world (after hooks)
inspect world *args:
    uv run -m scripts.inspect {{ world }} {{ args }}

# run any arbitrary script
run script *args:
    uv run -m {{ script }} {{ args }}

# generates default YAML options - same as "Generate Template Options" in AP launcher
gen-yamls:
    uv run -m scripts.gen_yamls
