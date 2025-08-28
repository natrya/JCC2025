image:
	docker build -t weebs .

chall:
	gcc -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wall -Wextra -fno-PIE -no-pie -o chal chal.c -Wl,-z,relro -Wl,-z,now -ldl 

deploy:
	docker run -d -p 127.0.0.1:4012:4012 -it weebs
