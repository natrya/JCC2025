## Writeup (Singkat)

Goals: Randomize a flag

Format `randomize.txt`:
```
FORMAT=V1
SEED=xxxxxx
ALGO=subst+spiral+perm
DATA=<32 hex>
```

Algoritma (di `soal.py`):
- Seed 6 digit diturunkan dari MD5: `int(md5,16) % 1_000_000`.
- Substitusi heksadesimal (bijektif) berdasarkan seed.
- Permutasi spiral pada matriks 4x8.
- Permutasi global random at seed.

Pembalikan (di `solver.py`):
- Baca seed dan data dari file.
- Reverse

Perintah:
```
# generate
python3 soal.py --out randomize.txt --flag flag.txt

# solve
python3 solver.py --dir . --file randomize.txt
```



