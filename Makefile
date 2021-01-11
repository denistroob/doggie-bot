run:
	docker build --no-cache -t doggie-bot:latest .
	docker-compose up --force-recreate

logs-script:
	sudo cat $(shell docker inspect --format='{{.LogPath}}' doggie-bot_script_1)

logs-db:
	sudo cat $(shell docker inspect --format='{{.LogPath}}' doggie-bot_doggies-db_1) 
