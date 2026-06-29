import os
from urllib.parse import urlparse

def parse_and_filter_data(input_file, keywords):
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' tidak ditemukan.")
        return

    print("=" * 60)
    print(f"{'RISSEC1337 || KEDIRISECTEAM':^60}")
    print(f"{'https://t.me/kedirisecteam1337':^60}")
    print("=" * 60)
    
    print(f"[*] Membaca data dari {input_file}...")
    print(f"[*] Keyword yang dicari: {', '.join(keywords)}")
    print("-" * 60)
    
    file_handlers = {}
    
    for kw in keywords:

        safe_kw = "".join(c for c in kw if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"hasil_{safe_kw.replace(' ', '_')}.txt"
        file_handlers[kw] = open(filename, 'w', encoding='utf-8')
        
        file_handlers[kw].write(f"{'Domain/URL':<50} | {'Username':<30} | {'Password'}\n")
        file_handlers[kw].write("-" * 100 + "\n")

    parsed_count = 0
    error_count = 0
    keyword_matches = {kw: 0 for kw in keywords}

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:

                    parts = line.rsplit(':', 2)
                    if len(parts) < 3:
                        print(f"[!] Baris {line_num} dilewati (Format salah): {line}")
                        error_count += 1
                        continue
                    
                    raw_url, username, password = parts[0], parts[1], parts[2]
                    
                    url_to_parse = raw_url if raw_url.startswith(('http://', 'https://')) else 'http://' + raw_url
                    domain = urlparse(url_to_parse).netloc
                    if not domain:
                        domain = raw_url

                    for kw in keywords:
                        if kw.lower() in domain.lower():
                        
                            file_handlers[kw].write(f"{domain:<50} | {username:<30} | {password}\n")
                            keyword_matches[kw] += 1
                            break # 
                        
                    parsed_count += 1

                except Exception as e:
                    print(f"[!] Gagal memproses baris {line_num}: {e}")
                    error_count += 1
                    
    finally:

        for handler in file_handlers.values():
            handler.close()

    print("-" * 60)
    print(f"[+] Selesai! Total baris diproses: {parsed_count}")
    print("[+] Rincian Hasil:")
    for kw, count in keyword_matches.items():
        print(f"    - Keyword '{kw}': {count} akun")
    if error_count > 0:
        print(f"[!] Baris error/dilewati: {error_count}")

if __name__ == "__main__":

    file_input = "list.txt"
    
    keyword_list = ["shopee.co.id", "x.com", "facebook.com", "google.com"]
    
    parse_and_filter_data(file_input, keyword_list)