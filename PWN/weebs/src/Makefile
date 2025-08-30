image:
	docker build -t weebs .

chall:
	gcc -O0 -fno-stack-protector -U_FORTIFY_SOURCE -Wall -Wextra -fPIE -pie -o chal chal.c -ldl 

deploy:
	docker run -d -p 127.0.0.1:4012:4012 -it weebs
