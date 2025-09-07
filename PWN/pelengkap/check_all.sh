#!/bin/bash
set -e

echo "[*] Checking all challenges..."

cd solver

# ret2shellcode
echo "[*] ret2shellcode..."
python3 solve_sesuatu.py > sesuatu.txt 2>&1 || true
grep -q "JCC25{stack_shellcode_success}" out_sesuatu.txt && echo "  [+] sesuatu OK" || echo "  [!] ret2shsesuatu FAIL"

# ret2win
echo "[*] ret2win..."
python3 solve_hore.py > out_hore.txt 2>&1 || true
grep -q "JCC25{ret2win_magic_button}" out_hore.txt && echo "  [+] hore OK" || echo "  [!] hore FAIL"

echo "[*] Done. See solver/out_*.txt for logs."

