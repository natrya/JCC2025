#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 4020

# Pertanyaan dan jawaban
challenges = [
    {
        "question": "Unauthorized Access, Server log mencatat banyak login gagal sebelum akhirnya ada yang berhasil.🕵️ Misi: Siapa nama user yang berhasil dibobol oleh attacker?",
        "answer": "student"
    },
    {
        "question": "Privilege Escalation,Attacker berhasil menaikkan hak akses menjadi root.🕵️ Misi: Dengan cara apa attacker mendapatkan akses root?",
        "answer": "sudo"
    },
    {
        "question": "Persistence Service,Attacker membuat service palsu agar tetap bisa masuk ke sistem.🕵️ Misi: Apa nama service yang dibuat attacker?",
        "answer": "system-update.service"
    },
    {
        "question": "Hidden Data,Attacker menyembunyikan file sensitif di dalam sebuah gambar.🕵️ Misi: Apa nama file gambar yang digunakan attacker?",
        "answer": "wallpaper.png"
    },
    {
        "question": "Secret Note,Ternyata ada file rahasia yang disembunyikan di dalam gambar tersebut.🕵️ Misi: File penting apa yang dicuri attacker?",
        "answer": "shadow"
    },
    {
        "question": "Memory loss,History perintah user tiba-tiba kosong.🕵️ Misi: Apa nama file history dari user yang dihapus isinya?",
        "answer": ".bash_history"
    },
    {
        "question": "Secret Tunnel,Attacker membuat tunnel untuk mengirim data keluar.🕵️ Misi: Port berapa yang digunakan attacker?",
        "answer": "8080"
    },
    {
        "question": "Hidden IP,IP milik attacker tersimpan di dalam informasi tunnel.🕵️ Misi: Berapa alamat IP attacker?",
        "answer": "192.168.217.128"
    }
]


def handle_client(conn, addr):
    conn.sendall(b"=== Infiltration of the Lab Server ===\n\n")
    while True:  # Loop terus jika salah
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
            # Kalau semua benar
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

