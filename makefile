build:
	docker build -t plohkoon/tr30:latest .

run: build
	docker run --rm --env-file .env plohkoon/tr30:latest
