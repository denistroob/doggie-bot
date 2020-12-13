run:
	docker build --no-cache -t doggie-bot:latest .
	docker-compose up --force-recreate
