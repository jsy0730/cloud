param([string]$pptx, [string]$outPath)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$out = [ordered]@{}
foreach ($sld in $pres.Slides) {
  foreach ($sh in $sld.Shapes) {
    if ($sh.Name -like 'm_*') {
      $tr = $sh.TextFrame2.TextRange
      $leg = $sh.TextFrame.TextRange
      $np = $leg.Paragraphs().Count
      $pl = New-Object System.Collections.ArrayList
      for ($i = 1; $i -le $np; $i++) {
        $pr = $leg.Paragraphs($i, 1)
        $n = $pr.Lines().Count
        $last = ([string]$pr.Lines($n, 1).Text).Trim()
        $words = @($last -split '[ \u00A0]+' | Where-Object { $_ -ne '' }).Count
        $len = ($last -replace '[\s\u00A0]', '').Length
        $null = $pl.Add([ordered]@{ n = $n; l = $len; w = $words })
      }
      $out[$sh.Name.Substring(2)] = [ordered]@{ h = [math]::Round([double]$tr.BoundHeight / 72.0, 4); w = [math]::Round([double]$tr.BoundWidth / 72.0, 4); pl = $pl }
    }
  }
}
$pres.Close(); $app.Quit()
$json = $out | ConvertTo-Json -Depth 5 -Compress
[System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
