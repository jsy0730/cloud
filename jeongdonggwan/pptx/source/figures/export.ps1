param([string]$pptx,[string]$outdir)
$ErrorActionPreference='Stop'
if(Test-Path $outdir){Remove-Item $outdir -Recurse -Force}
New-Item -ItemType Directory -Path $outdir | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$pres.Export($outdir, 'PNG', 1920, 1080)
$pres.Close()
$app.Quit()
