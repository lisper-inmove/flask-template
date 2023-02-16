update-submodule:
	git submodule update --init --recursive
dev:
	bash bin/dev.sh
gdev:
	bash bin/gdev.sh
cgp:
	mkdir gproto
	touch gproto/api.proto
	echo 'syntax = "proto3";' > gproto/api.proto
clear-cgp:
	rm -rf gproto
