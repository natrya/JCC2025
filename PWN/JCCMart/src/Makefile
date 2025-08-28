image:
	docker build -t jccmart .

chall:
	gcc -fstack-protector -o chall chall.c 

deploy:
	docker run -d -p 127.0.0.1:4008:4008 -it jccmart
