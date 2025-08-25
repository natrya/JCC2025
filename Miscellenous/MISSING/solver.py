import hashlib
import string 
import random 


md5_sum = "19387e6814a3db8ce32d58085b12b9d1"
flag_find = "{}5878740f095608{}398860d73a1e{}57f3d22d09be999{}427f74eae9851ab3e5{}"
#real_flag = "e5878740f095608e398860d73a1eb57f3d22d09be9995427f74eae9851ab3e54"

#pool = string.ascii_letters + string.digits 
pool = "eeb54"

while True:
    flag = flag_find.format(random.choice(pool), random.choice(pool), random.choice(pool), random.choice(pool), random.choice(pool))
    if hashlib.md5(flag.encode()).hexdigest() == md5_sum:
        print(flag)
        break