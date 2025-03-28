# Markdown'dan PDF'e Dönüştürme Scripti

$inputFile = $args[0]
$outputFile = $args[1]

if (-not $inputFile -or -not $outputFile) {
    Write-Host "Kullanım: .\convert.ps1 <input_file> <output_file>"
    exit 1
}

$inputBaseName = [System.IO.Path]::GetFileNameWithoutExtension($inputFile)
$outputPath = "input/$inputBaseName.pdf"

if (-not $outputFile) {
    $outputFile = $outputPath
}

Write-Host "Dönüştürülüyor: $inputBaseName.md -> $([System.IO.Path]::GetFileName($outputFile))"

pandoc $inputFile -o $outputFile --pdf-engine=wkhtmltopdf

if ($LASTEXITCODE -eq 0) {
    Write-Host "Başarılı: $([System.IO.Path]::GetFileName($outputFile)) oluşturuldu"
} else {
    Write-Host "Hata: PDF oluşturulamadı!"
    exit 1
}

Write-Host "`nİşlem tamamlandı!" 