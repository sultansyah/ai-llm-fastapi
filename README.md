# api-ai-llm-fastapi-ollama

## 🚀 Cara Menjalankan Proyek

### 1️⃣ Instalasi Dependensi

Pastikan kamu sudah menginstal semua library yang dibutuhkan dengan perintah berikut:

```bash
pip install -r requirements.txt
```

### 2️⃣ Menyiapkan Environment (UV Python)

Buat virtual environment menggunakan `uv` atau alat environment lain yang kamu pakai. Contohnya:

```bash
uv env create .uv       # membuat environment
uv activate .uv        # aktifkan environment
```

Salin file `.env-example` menjadi `.env` dan isi `API_KEY` sesuai kebutuhan:

```bash
cp .env-example .env   # Linux/macOS
copy .env-example .env  # Windows
```

Edit `.env` jika perlu dan isi `API_KEY`:

```env
API_KEY=masukkan_api_key_anda_di_sini
```

### 3️⃣ Menjalankan Aplikasi

Setelah environment aktif dan semua dependensi terinstal, jalankan server FastAPI dengan perintah:

```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000` secara default.

### 4️⃣ Struktur Proyek

Berikut struktur proyek saat ini:

```
api-ai-llm-fastapi-ollama/
├─ .env
├─ .env-example
├─ .gitignore
├─ main.py
├─ pyproject.toml
├─ README.md
├─ requirements.txt
└─ uv.lock
```