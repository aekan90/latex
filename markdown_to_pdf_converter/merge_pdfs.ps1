# PDF Birleştirme Scripti

Write-Host "PDF'ler birleştiriliyor..."

# LaTeX ile PDF'leri birleştir
xelatex kitap_template.tex

# Başarılı olup olmadığını kontrol et
if ($LASTEXITCODE -eq 0) {
    # Oluşturulan PDF'i output klasörüne taşı
    Move-Item -Path "kitap_template.pdf" -Destination "output/birlesik.pdf" -Force
    Write-Host "PDF'ler başarıyla birleştirildi: output/birlesik.pdf"
    
    # Geçici dosyaları temizle
    Remove-Item "kitap_template.*" -Force
} else {
    Write-Host "Hata: PDF'ler birleştirilemedi!"
    exit 1
}

Write-Host "`nİşlem tamamlandı!" 