# AI-LLM-FastAPI

This project is an AI-powered chatbot application that uses FastAPI, Ollama, LangChain, and ChromaDB for semantic search and question answering. It processes customer reviews stored in a CSV file using vector embeddings and provides context-aware responses through an LLM with short-term memory capabilities.

## 🚀 Cara Menjalankan Proyek

### 1️⃣ Instalasi Dependensi

Pastikan kamu sudah menginstal semua library yang dibutuhkan dengan perintah berikut:

```bash
pip install -r requirements.txt
```

### 2️⃣ Menyiapkan Environment dan Konfigurasi

Salin file `.env-example` menjadi `.env` dan isi konfigurasi sesuai kebutuhan:

```bash
cp .env-example .env   # Linux/macOS
copy .env-example .env  # Windows
```

Edit `.env` dan isi variabel konfigurasi:

```env
MODEL=                # Nama model Ollama yang akan digunakan (e.g., llama3, mistral)
CSV_PATH=file.csv     # Path ke file CSV yang berisi review pelanggan
DB_PATH=chrome_db     # Direktori untuk menyimpan database vektor Chroma
MODEL_EMBEDDING=      # Model embedding Ollama (e.g., nomic-embed-text, mxbai-embed-large)
COLLECTION_NAME=collection_name   # Nama koleksi Chroma
SEARCH_TYPE=mmr       # Tipe pencarian (mmr, similarity, dsb)
SEARCH_KWARGS_K=5     # Jumlah dokumen yang akan diambil saat pencarian
MAX_MEMORY=10         # Jumlah maksimal pesan dalam memori sesi (termasuk user dan assistant)
```

Pastikan kamu memiliki Ollama terinstal dan model yang dibutuhkan.

### 3️⃣ Menjalankan Aplikasi

Setelah environment aktif dan semua dependensi terinstal, jalankan server FastAPI dengan perintah:

```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000` secara default. Akses aplikasi melalui browser untuk membuka antarmuka chat.

## ⚙️ Fitur Utama

1. **Pencarian Semantik** - Menggunakan vektor embeddings untuk mencari review pelanggan yang paling relevan
2. **Memori Sesi** - Menyimpan riwayat percakapan dalam jangka pendek untuk konteks percakapan yang lebih baik
3. **Streaming Jawaban** - Jawaban dari LLM dikirim dalam bentuk streaming (Server-Sent Events) untuk pengalaman real-time
4. **Antarmuka Web** - Antarmuka chat yang menampilkan percakapan pengguna dan AI dalam bentuk bubble chat
5. **Pembatasan Topik** - Aplikasi hanya menjawab pertanyaan terkait restoran pizza sesuai dengan aturan yang ditentukan dalam prompt

## 🛠️ Cara Kerja Aplikasi

Aplikasi ini bekerja dengan cara:

1. Membaca file CSV yang berisi review pelanggan
2. Mengonversi teks review menjadi vektor menggunakan model embedding
3. Menyimpan vektor ke dalam database Chroma untuk pencarian semantik
4. Saat pengguna mengajukan pertanyaan:
   - Menyimpan pesan pengguna ke memori sesi
   - Membangun prompt kontekstual dari riwayat percakapan
   - Mencari review yang paling relevan dari database vektor
   - Menggabungkan review yang relevan dengan pertanyaan dan konteks percakapan
   - Mengirimkan ke LLM untuk mendapatkan jawaban kontekstual
5. Mengembalikan jawaban dalam bentuk streaming (Server-Sent Events)
6. Menyimpan jawaban LLM ke memori sesi untuk percakapan selanjutnya

Antarmuka web menyediakan antarmuka chat real-time yang menampilkan percakapan pengguna dan AI dengan efek streaming serta memori kontekstual.