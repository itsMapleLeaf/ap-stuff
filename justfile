worlds_dirname := "manual_worlds"

games_dir := justfile_directory() / "games"
dist_dir := justfile_directory() / "dist"
generate_dir := dist_dir / "generate"
generate_players_dir := dist_dir / "generate/players"

user_archipelago_dir := 'C:/ProgramData/Archipelago'
archipelago_generate := user_archipelago_dir / "ArchipelagoGenerate.exe"
archipelago_server := user_archipelago_dir / "ArchipelagoServer.exe"

export PYTHONPATH := justfile_directory() / "archipelago"

# build specified local manual worlds into the Archipelago custom_worlds folder
build *args:
    echo "\n" | uv run -m scripts.build {{ args }}

# generate and serve a multiworld for a given multi
play multi: (generate multi) serve

# generate a multiworld with a given multiworld config
generate multi: (build "--multi" multi)
    echo "\n" | uv run -m scripts.generate {{ multi }}

# serve a generated multiworld
serve:
    cd "{{ generate_dir }}"; {{ archipelago_server }} *.archipelago

# create apworlds and a stitched config for a multi
export multi:
    uv run -m scripts.export {{ multi }}

# create a new manual world
create world:
    cp -r template/src manual_worlds/{{ world }}

# print the data for a world (after hooks)
inspect world *args:
    uv run -m scripts.inspect {{ world }} {{ args }}

# run any arbitrary script
[positional-arguments]
run script *args:
    # passes arguments verbatim, supporting quoted arguments with spaces
    uv run -m "$@"

# generates default YAML options - same as "Generate Template Options" in AP launcher
gen-yamls:
    uv run -m scripts.gen_yamls

mkconfig world:
    echo "todo"
    # uv run -m scripts.create_config {{ world }}

saika-dev:
    PYTHONPATH="universal_tracker" uv run -m saika
