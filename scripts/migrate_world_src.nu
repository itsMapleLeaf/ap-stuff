for world_folder in (ls ./manual_worlds/*) {
	do {
		if !(src | path exists) {
			continue
		}
		try {rm -r ...(ls $world_folder.name | where { ($in.name | path basename) != src } | get name)}
		cd $world_folder.name
		mv src/**/* .
		rm -r src
	}
}
