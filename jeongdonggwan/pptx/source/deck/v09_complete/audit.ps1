param([string]$pptx, [string]$outPath)
# overflow / collision audit through PowerPoint itself (the same layout engine the viewer uses)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$SW = $pres.PageSetup.SlideWidth; $SH = $pres.PageSetup.SlideHeight
$res = New-Object System.Collections.ArrayList
foreach ($sld in $pres.Slides) {
  $n = $sld.SlideIndex
  $boxes = New-Object System.Collections.ArrayList
  foreach ($sh in $sld.Shapes) {
    $isTable = $false
    try { $isTable = [bool]$sh.HasTable } catch {}
    if ($isTable) {
      $bottom = ($sh.Top + $sh.Height) / 72.0
      $null = $res.Add([ordered]@{ slide = $n; kind = 'table'; name = $sh.Name; bottom = [math]::Round($bottom, 3); right = [math]::Round(($sh.Left + $sh.Width) / 72.0, 3) })
      continue
    }
    $has = $false
    try { $has = [bool]($sh.HasTextFrame -and $sh.TextFrame.HasText) } catch {}
    if (-not $has) { continue }
    $tr = $sh.TextFrame2.TextRange
    $txt = [string]$tr.Text
    if ($txt.Trim().Length -eq 0) { continue }
    $bh = [double]$tr.BoundHeight; $bw = [double]$tr.BoundWidth
    $bt = [double]$tr.BoundTop; $bl = [double]$tr.BoundLeft
    $over = $bh - [double]$sh.Height
    $wrapOn = [bool]($sh.TextFrame2.WordWrap)
    $null = $res.Add([ordered]@{ slide = $n; kind = 'text'; name = $sh.Name; text = $txt.Substring(0, [math]::Min(24, $txt.Length)); boxH = [math]::Round($sh.Height / 72.0, 3); textH = [math]::Round($bh / 72.0, 3);
        over = [math]::Round($over / 72.0, 3); bl = [math]::Round($bl / 72.0, 3); bt = [math]::Round($bt / 72.0, 3); bw = [math]::Round($bw / 72.0, 3); bh = [math]::Round($bh / 72.0, 3);
        right = [math]::Round(($bl + $bw) / 72.0, 3); bottom = [math]::Round(($bt + $bh) / 72.0, 3); wrap = $wrapOn })
  }
}
$pres.Close(); $app.Quit()
$json = $res | ConvertTo-Json -Depth 4 -Compress
[System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
