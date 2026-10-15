param([string]$src, [string]$pdf, [string]$embed)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($src, $false, $false, $false)
$pres.SaveCopyAs($embed, 24, -1)
$pres.SaveAs($pdf, 32)
$pres.Close(); $app.Quit()
