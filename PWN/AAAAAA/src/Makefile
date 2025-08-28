image:
	docker build -t scream .

chall:
	gcc -fno-stack-protector -o chall chall.c -Wno-implicit-function-declaration

deploy:
	docker run -d -p 127.0.0.1:5001:1337 -it scream