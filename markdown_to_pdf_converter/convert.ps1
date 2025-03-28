# Markdown'dan PDF'e Dönüştürme Scripti

$inputFile = "4_KITAP_DUZENLENMIS_METIN.md"
$outputFile = "kitap.pdf"
$muskaFile = "muska.pdf"
$finalOutput = "birlesik.pdf"

Write-Host "Dönüştürülüyor: $inputFile -> $outputFile"

# Markdown'ı PDF'e dönüştür
pandoc $inputFile --pdf-engine=xelatex -V geometry:margin=2.54cm -V mainfont="Times New Roman" -V fontsize=12pt -V documentclass=book -V papersize=a4 -o $outputFile --toc --toc-depth=3 --number-sections -V dir=rtl --include-in-header=header.tex

if ($LASTEXITCODE -eq 0) {
    Write-Host "Başarılı: $outputFile oluşturuldu"
} else {
    Write-Host "Hata: PDF oluşturulamadı!"
    exit 1
}

# PDF'leri birleştir
Write-Host "`nPDF'ler birleştiriliyor..."

# LaTeX dosyası oluştur
$texContent = @"
\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{pdfpages}

\begin{document}
\includepdf[pages=-]{$outputFile}
\includepdf[pages=-]{$muskaFile}
\end{document}
"@

# Geçici .tex dosyası oluştur
$texContent | Out-File -FilePath "temp_merge.tex" -Encoding UTF8

# LaTeX ile PDF'leri birleştir
xelatex temp_merge.tex

# Başarılı olup olmadığını kontrol et
if ($LASTEXITCODE -eq 0) {
    # Oluşturulan PDF'i taşı
    Move-Item -Path "temp_merge.pdf" -Destination $finalOutput -Force
    Write-Host "PDF'ler başarıyla birleştirildi: $finalOutput"
    
    # Geçici dosyaları temizle
    Remove-Item "temp_merge.*" -Force
} else {
    Write-Host "Hata: PDF'ler birleştirilemedi!"
    exit 1
}

Write-Host "`nİşlem tamamlandı!" 