# PDF Birleştirme Scripti

# PDF dosyalarının yolları
$pdf1 = "input/kitap.pdf"
$pdf2 = "input/muska.pdf"
$outputFile = "output/birlesik.pdf"

Write-Host "PDF'ler birleştiriliyor..."

# LaTeX dosyası oluştur
$texContent = @"
\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{pdfpages}

\begin{document}
\includepdf[pages=-]{$pdf1}
\includepdf[pages=-]{$pdf2}
\end{document}
"@

# Geçici .tex dosyası oluştur
$texContent | Out-File -FilePath "temp_merge.tex" -Encoding UTF8

# LaTeX ile PDF'leri birleştir
xelatex temp_merge.tex

# Başarılı olup olmadığını kontrol et
if ($LASTEXITCODE -eq 0) {
    # Oluşturulan PDF'i output klasörüne taşı
    Move-Item -Path "temp_merge.pdf" -Destination $outputFile -Force
    Write-Host "PDF'ler başarıyla birleştirildi: $outputFile"
    
    # Geçici dosyaları temizle
    Remove-Item "temp_merge.*" -Force
} else {
    Write-Host "Hata: PDF'ler birleştirilemedi!"
    exit 1
}

Write-Host "`nİşlem tamamlandı!" 