image:
	docker build -t ew .

chall:
	gcc -fno-stack-protector -o chall chall.c 

deploy:
	docker run -d -p 127.0.0.1:5002:1337 -it ew