#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 4018

# Pertanyaan dan jawaban
challenges = [
    {
        "question": "Lampiran Berbahaya, File jadwal_kelas.docx ditemukan di email. 🕵️ Misi: Temukan hash MD5 dari file tersebut.",
        "answer": "A0A41C4FEA0D9EDA3D7B4C7807AE202A"
    },
    {
        "question": "Shortcut Palsu, Terdapat file jadwal.lnk yang mencurigakan.🕵️ Misi: Bongkar shortcut ini dan temukan URL berbahaya di dalamnya.",
        "answer": "http://voters-wear-genuine-pure.trycloudflare.com"
    },
    {
        "question": "Jejak Browser, Siswa ternyata diarahkan ke sebuah website mencurigakan. 🕵️ Misi: Cari tahu domain apa yang dikunjungi",
        "answer": "http://control-r3dpanda.net/"
    },
    {
        "question": "Login Misterius, Event log menunjukkan ada login aneh ke komputer.🕵️ Misi: Siapa username yang dipakai penyerang untuk login? dan berapa IP Address yang digunakan? format jawaban login:IP",
        "answer": "student01:192.168.146.137"
    },
    {
        "question": "File Rahasia Terkunci, Sebuah file nilai_siswa.zip ditemukan dalam keadaan terkunci.🕵️ Misi: Buka dan temukan isi pesan rahasia di dalam file exfil.txt.",
        "answer": "DATA_EXFIL_SUCCESS"
    }
]


def handle_client(conn, addr):
    conn.sendall(b"=== Cyber Forensics Challenge ===\n\n")
    while True:  # ulangi terus sampai jawaban benar semua
        for chal in challenges:
            conn.sendall(f"{chal['question']}\nJawabanmu: ".encode())
            data = conn.recv(4096)
            if not data:
                conn.close()
                return
            user_input = data.decode().strip()
            if user_input != chal["answer"]:
                conn.sendall("❌ Jawaban salah. Mengulang dari awal...\n\n".encode())
                break  # restart dari awal
            else:
                conn.sendall("✅ Benar!\n\n".encode())
        else:
            # semua pertanyaan benar
            try:
                with open("flag.txt", "r") as f:
                    flag = f.read().strip()
                conn.sendall(f"🎉 Selamat! Ini flag kamu: {flag}\n".encode())
            except FileNotFoundError:
                conn.sendall("Flag file tidak ditemukan!\n".encode())
            conn.close()
            return


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()


if __name__ == "__main__":
    main()

