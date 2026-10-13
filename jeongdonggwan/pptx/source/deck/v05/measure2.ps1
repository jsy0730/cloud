param([string]$pptx, [string]$outPath)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$out = [ordered]@{}
foreach ($sld in $pres.Slides) {
  foreach ($sh in $sld.Shapes) {
    if ($sh.Name -like 'm_*') {
      $tr = $sh.TextFrame2.TextRange
      $out[$sh.Name.Substring(2)] = [ordered]@{ h = [math]::Round([double]$tr.BoundHeight / 72.0, 4); w = [math]::Round([double]$tr.BoundWidth / 72.0, 4) }
    }
  }
}
$pres.Close(); $app.Quit()
$json = $out | ConvertTo-Json -Depth 4 -Compress
[System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
