#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 4017

# Pertanyaan dan jawaban
challenges = [
    {
        "question": "File Metadata, Ternyata ada file jadwal_kelas.docx di dalam USB.🕵️ Misi: Cari tahu siapa pembuat (author / creator) file tersebut.",
        "answer": "R3dPanda"
    },
    {
        "question": "Deleted File, Ada file yang sempat dihapus di Recycle Bin USB. 🕵️ Misi: Pulihkan file tersebut dan cari tahu isi dari filenya.",
        "answer": "C00l_Y0u_F1nD_M3"
    },
    {
        "question": "Hidden Note, Salah satu gambar menyimpan pesan rahasia di metadata. 🕵️ Misi: Bongkar metadata gambar dan temukan isi pesan rahasianya.",
        "answer": "Hi,R3dPanda was here..."
    },
    {
        "question": "Suspicious Shortcut, Ada shortcut game.lnk yang terlihat mencurigakan. 🕵️ Misi: Cari tahu alamat url yang dijalankan oleh shortcut itu.",
        "answer": "http://wear-voters-genuine-pure.trycloudflare.com"
    },
    {
        "question": "Clue in USBSTOR. Dari artefak Registry SYSTEM, terlihat USB ini pernah dicolok ke komputer lab. 🕵️ Misi: Temukan Serial Number dari USB tersebut.",
        "answer": "1234567890ABCDEF"
    }
]


def handle_client(conn, addr):
    conn.sendall(b"=== USB Forensics Challenge ===\n\n")
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

