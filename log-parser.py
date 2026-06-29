import os

def parse_to_separate_files(input_file, keywords):
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' tidak ditemukan.")
        return

    print("=" * 50)
    print(f"{'DATA PARSER & FILTER BY RISSEC1337':^50}")
    print("=" * 50)
    print(f"[*] Membaca data dari: {input_file}")
    print(f"[*] Keyword yang dicari: {', '.join(keywords)}")
    print("-" * 50)

    # Membuat dictionary untuk menyimpan file handler berdasarkan keyword
    file_handlers = {}
    keyword_matches = {kw: 0 for kw in keywords}
    
    # Siapkan file output untuk setiap keyword
    for kw in keywords:
        # Membersihkan nama file dari karakter non-alfanumerik agar aman bagi sistem operasi
        safe_kw = "".join(c for c in kw if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"hasil_{safe_kw.replace(' ', '_')}.txt"
        file_handlers[kw] = open(filename, 'w', encoding='utf-8')

    parsed_count = 0
    error_count = 0

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Memisahkan format url:user:pass dari kanan
                    parts = line.rsplit(':', 2)
                    if len(parts) < 3:
                        error_count += 1
                        continue
                    
                    raw_url, username, password = parts[0], parts[1], parts[2]
                    
                    # Pengecekan keyword pada URL
                    for kw in keywords:
                        if kw.lower() in raw_url.lower():
                            # Menulis ke file spesifik keyword dengan format pipa (|)
                            file_handlers[kw].write(f"{raw_url}|{username}|{password}\n")
                            keyword_matches[kw] += 1
                            break # Berhenti mengecek keyword lain jika sudah cocok
                        
                    parsed_count += 1

                except Exception as e:
                    print(f"[!] Gagal memproses baris {line_num}: {e}")
                    error_count += 1
                    
    finally:
        # Wajib menutup semua file handler yang telah dibuka
        for handler in file_handlers.values():
            handler.close()

    # Laporan Akhir
    print("-" * 50)
    print(f"[+] Selesai! Total baris diproses: {parsed_count}")
    print("[+] Rincian Hasil per File:")
    for kw, count in keyword_matches.items():
        print(f"    - Keyword '{kw}': {count} baris")
    if error_count > 0:
        print(f"[!] Baris error/dilewati: {error_count}")

if __name__ == "__main__":
    file_input = "list.txt"
    
    keyword_list = [ 
        "google.com",
        "shopee.co.id",
        "facebook.com"
    ]
    
    parse_to_separate_files(file_input, keyword_list)
