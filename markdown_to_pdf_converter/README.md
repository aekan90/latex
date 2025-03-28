# Markdown'dan PDF'e Dönüştürücü

Bu araç, Markdown formatındaki metni profesyonel görünümlü bir PDF kitaba dönüştürür ve başka bir PDF ile birleştirir.

## Özellikler

- Times New Roman yazı tipi
- 12 punto yazı boyutu
- 1.5 satır aralığı
- 2.54 cm (1 inç) sayfa kenar boşlukları
- Otomatik sayfa numaralandırma (alt orta)
- İçindekiler tablosu
- Bölüm numaralandırma
- Türkçe ve Arapça karakter desteği
- Profesyonel kitap formatı
- PDF birleştirme özelliği

## Gereksinimler

- PowerShell
- Pandoc
- XeLaTeX (MiKTeX veya TeX Live)
- Times New Roman yazı tipi
- Amiri yazı tipi (Arapça metinler için)

## Çalışan Prompt

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\convert.ps1
```

Bu komut şu işlemleri gerçekleştirir:
1. PowerShell güvenlik politikasını geçici olarak ayarlar
2. Markdown dosyasını PDF'e dönüştürür
3. Oluşturulan PDF'i muska.pdf ile birleştirir

## Dosya Yapısı

```
markdown_to_pdf_converter/
│
├── convert.ps1           # Dönüştürme ve birleştirme betiği
├── header.tex           # LaTeX başlık ayarları
├── 4_KITAP_DUZENLENMIS_METIN.md  # Kaynak markdown dosyası
└── muska.pdf            # Birleştirilecek PDF dosyası
```

## Dosya İçerikleri

### convert.ps1
```powershell
# Markdown'dan PDF'e Dönüştürme Scripti
$inputFile = "4_KITAP_DUZENLENMIS_METIN.md"
$outputFile = "kitap.pdf"
$muskaFile = "muska.pdf"
$finalOutput = "birlesik.pdf"

# Markdown'ı PDF'e dönüştür
pandoc $inputFile --pdf-engine=xelatex -V geometry:margin=2.54cm -V mainfont="Times New Roman" -V fontsize=12pt -V documentclass=book -V papersize=a4 -o $outputFile --toc --toc-depth=3 --number-sections -V dir=rtl --include-in-header=header.tex
```

### header.tex
```latex
\usepackage{polyglossia}
\setmainlanguage{turkish}
\setotherlanguage{arabic}
\newfontfamily\arabicfont[Script=Arabic]{Amiri}
\newfontfamily\turkishfont{Times New Roman}
\usepackage{bidi}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
```

## Çıktı Dosyaları

1. `kitap.pdf`: Markdown'dan dönüştürülen PDF
2. `birlesik.pdf`: kitap.pdf ve muska.pdf birleştirilmiş hali

## Notlar

- Markdown dosyası UTF-8 formatında olmalıdır
- Arapça metinler için RTL desteği mevcuttur
- PDF'de sayfa numaraları ortalanmış olarak alt kısımda görünür
- İçindekiler tablosu otomatik olarak oluşturulur
- Bölüm başlıkları otomatik olarak numaralandırılır
- Birleştirme işlemi sırasında sayfa numaraları korunur
- Üst bilgi çizgisi kaldırıldı (daha temiz görünüm için)

## Hata Giderme

Eğer dönüştürme sırasında hata alırsanız:

1. PowerShell'i yönetici olarak çalıştırın
2. Gerekli yazılımların yüklü olduğundan emin olun:
   - Pandoc: `pandoc --version`
   - XeLaTeX: `xelatex --version`
3. Markdown dosyasının UTF-8 formatında olduğunu kontrol edin
4. muska.pdf dosyasının mevcut olduğunu kontrol edin
5. Times New Roman ve Amiri yazı tiplerinin sistemde yüklü olduğunu kontrol edin

## Lisans

Bu araç MIT lisansı altında dağıtılmaktadır.
