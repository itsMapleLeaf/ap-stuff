create WORLD:
	git subtree add --prefix worlds/{{WORLD}} template main

update WORLD:
	git subtree pull --prefix worlds/{{WORLD}} template main
