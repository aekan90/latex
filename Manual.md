# LaTeX Kitap Projesi Manueli

## İçindekiler
1. [İsimlendirme Standartları](#1-isimlendirme-standartlari)
2. [Klasör Yapısı](#2-klasör-yapisi)
3. [Adım Adım Kitap Oluşturma](#3-adim-adim-kitap-olusturma)
4. [Script Kullanımı](#4-script-kullanimi)

## 1. İsimlendirme Standartları

### Klasör İsimleri
- Türkçe karakter kullanılmaz
- PascalCase formatında (örn: KaynakMetinler, TexDosyalari)
- Boşluk kullanılmaz
- Her kelime büyük harfle başlar

### Dosya İsimleri
- Türkçe karakter kullanılmaz
- Format: `[Sıra]_[DOSYA_ADI].[uzantı]`
- Sıra: 0'dan başlayan numara (örn: 0_, 1_, 2_)
- Dosya Adı: BÜYÜK_HARF_VE_ALTÇIZGI
- Uzantı: Küçük harf (.txt, .tex, .pdf)

### Proje İsimleri
- Türkçe karakter kullanılmaz
- Format: `[Sıra]_[PROJE_ADI]`
- Sıra: İki basamaklı numara (01_, 02_, vb.)
- Proje Adı: BÜYÜK_HARF_VE_ALTÇIZGI

## 2. Klasör Yapısı

### Ana Dizin
```
[ANA_DIZIN]\                                # Ana kitap projeleri dizini
├── 01_KURANDAN_KORUCU_AYETLER_VE_SIFA_DUALARI\  # 1. Kitap Projesi
├── 02_[PROJE_ADI]\                        # 2. Kitap Projesi
├── 03_[PROJE_ADI]\                        # 3. Kitap Projesi
└── ORTAK_KAYNAKLAR\                       # Tüm projelerde kullanılacak ortak dosyalar
```

### Proje Dizini
```
[XX_PROJE_ADI]\                            # Her proje klasörü
├── KaynakMetinler\                        # Kaynak metin dosyaları
│   ├── Bolumler\                         # Bölümlere ayrılmış metinler
│   └── Backup\                          # Yedek dosyaları
├── TexDosyalari\                          # LaTeX dosyaları
│   ├── Bolumler\                         # Bölüm TeX dosyaları
│   ├── PdfFiles\                         # PDF çıktıları
│   └── TempFiles\                        # Geçici dosyalar
└── PythonScripts\                         # Python scriptleri
```

## 3. Adım Adım Kitap Oluşturma

### 1. Yeni Proje Oluşturma
1. Cursor IDE'yi açın
2. Sol panelde "Chat" sekmesine tıklayın
3. "New Chat" butonuna tıklayın
4. Prompt:
   ```
   PROJE YAPISI VE KULLANIM REHBERİNE UYARAK [PROJE_DIZINI] klasöründe [PROJE_ADI] isimli yeni bir kitap projesi oluşturur musun?
   ```

### 2. Ham Metin Yerleştirme
1. Metin dosyasını `[PROJE_DIZINI]/[PROJE_ADI]/KaynakMetinler` klasörüne kopyalayın
2. Cursor IDE'de dosyayı açın
3. Sağ tıklayın ve "Add to Chat" seçin
4. Prompt:
   ```
   [PROJE_DIZINI]/[PROJE_ADI]/KaynakMetinler klasöründeki [DOSYA_ADI] dosyasını 0_KITAP_KAYNAK_METIN.txt olarak yeniden adlandır.
   ```

### 3. Ana Metin Dosyasını Düzenleme (.md veya .txt)
1. Cursor'da yeni chat başlatın
2. Kaynak dosyayı açın ve içeriği seçin
3. Prompt:
   ```
   [KAYNAK_DOSYA] dosyasını okuyarak:
   - Gereksiz satır boşluklarını temizle
   - Başlık formatlarını standartlaştır
   - Paragraf girintilerini düzenle
   - Noktalama işaretlerini kontrol et
   Düzenlenmiş metni [YENI_VERSIYON]_KITAP_DUZENLENMIS_METIN.md olarak kaydet.
   ```

### 4. Ana Metni Bölümlere Ayırma
1. Cursor'da yeni chat başlatın
2. Düzenlenmiş metni açın
3. Prompt:
   ```
   [TAM_DOSYA_YOLU] dosyasını incele ve:
   - Başlıkları tespit et
   - Her başlığı '# ' ile işaretle
   - [PROJE_DIZINI]/PythonScripts/split_file.py scriptini kullanarak bölümlere ayır
   - Bölümleri [PROJE_DIZINI]/KaynakMetinler/Bolumler klasörüne kaydet
   ```

4 den 5 e geçerken tex dosyalarınızda hiç bir problem olmaması gerekiyor.
tex dosyalarınızı ön izleyebilmeniz gerek.

### 5. Bölümleri LaTeX'e Dönüştürme
1. Cursor'da yeni bir chat başlatın
2. Aşağıdaki komutu kullanın:
   ```bash
   python "PythonScripts/md_to_tex.py" "[PROJE_DIZINI]"
   ```
3. Script otomatik olarak:
   - Gerekli dizin yapısını kontrol eder ve eksik dizinleri oluşturur
   - Mevcut TeX dosyalarını yedekler
   - KaynakMetinler/Bolumler klasöründeki Markdown dosyalarını LaTeX'e dönüştürür
   - Dönüştürülen LaTeX dosyalarını TexDosyalari/Bolumler klasörüne kaydeder
   - main.tex dosyasını oluşturur

4. Script tamamlandıktan sonra, PDF oluşturmak için:
   ```bash
   cd "TexDosyalari"
   xelatex main.tex
   ```

### 6. PDF Oluşturma
1. Cursor'da yeni chat başlatın
2. Prompt:
   ```
   [PROJE_DIZINI]/[PROJE_ADI] klasöründe:
   - [PROJE_DIZINI]/PythonScripts/compile_tex_to_pdf.py scriptini çalıştırarak 
    TexDosyalari/Bolumler dizinindeki tex dosyalarından aynı isimde PDF dosyalarını oluştur
   - Oluşturulan PDF'i TexDosyalari/PdfFiles klasöründe kontrol et
   ```

## 4. Script Kullanımı

### split_file.py
```bash
python [PROJE_DIZINI]/PythonScripts/split_file.py "[TAM_DOSYA_YOLU]" "[PROJE_DIZINI]/KaynakMetinler/Bolumler"
```

### md_to_tex.py
```bash
python [PROJE_DIZINI]/PythonScripts/md_to_tex.py "[PROJE_DIZINI]"
```

### compile_tex_to_pdf.py
```bash
# Tek dosya derleme
python compile_tex_to_pdf.py "[PROJE_DIZINI]" --tex-file "[DOSYA_ADI]"

# Tüm dosyaları derleme
python compile_tex_to_pdf.py "[PROJE_DIZINI]"
```

### Çıktı Dizinleri
- PDF Çıktıları: `TexDosyalari` (ana dizin)
- Geçici Dosyalar: `TexDosyalari/TempFiles`
  * .aux: Yardımcı dosyalar
  * .log: Log dosyaları
  * .out: Çıktı dosyaları
  * .toc: İçindekiler dosyaları
  * .synctex.gz: Senkronizasyon dosyaları
  * .tfm: Font metrik dosyaları
  * .600gf: Font dosyaları 