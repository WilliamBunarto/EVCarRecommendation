import requests
import json

# URL API Flask yang sudah Anda buat
url = 'http://localhost:5000/rekomendasi-mobil'

# Data yang akan dikirim ke API
data = {
    "umur": 30,
    "gaya": "modern dan minimalis",
    "pekerjaan": "software engineer"
}

# Mengirim request POST ke API
response = requests.post(url, json=data)

# Mengecek status code dan menampilkan hasil
if response.status_code == 200:
    rekomendasi = response.json().get('rekomendasi')
    print(f"Rekomendasi Mobil Listrik: {rekomendasi}")
else:
    print(f"Error: {response.status_code} - {response.text}")
