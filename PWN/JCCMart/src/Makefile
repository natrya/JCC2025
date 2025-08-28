image:
	docker build -t jccmart .

chall:
	gcc -fstack-protector -o chall chall.c 

deploy:
	docker run -d -p 127.0.0.1:5005:1337 -it jccmart