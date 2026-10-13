param([string]$pptx, [string]$outPath)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$res = New-Object System.Collections.ArrayList
function scan($sh, $slideIdx, $label) {
  $has = $false
  try { $has = [bool]($sh.HasTextFrame -and $sh.TextFrame.HasText) } catch {}
  if (-not $has) { return }
  $tr = $sh.TextFrame.TextRange
  $np = $tr.Paragraphs().Count
  for ($i = 1; $i -le $np; $i++) {
    $pr = $tr.Paragraphs($i, 1)
    $txt = ([string]$pr.Text).Trim()
    if ($txt.Length -lt 6) { continue }
    $n = $pr.Lines().Count
    if ($n -lt 2) { continue }
    $last = ([string]$pr.Lines($n, 1).Text).Trim()
    $words = @($last -split '[  ]+' | Where-Object { $_ -ne '' }).Count
    $len = $last.Length
    if (($words -le 1 -and $len -le 5) -or $len -le 2) {
      $null = $res.Add([ordered]@{ slide = $slideIdx; shape = $sh.Name; para = $i; lines = $n; last = $last; text = $txt.Substring(0, [math]::Min(40, $txt.Length)) })
    }
  }
}
foreach ($sld in $pres.Slides) {
  foreach ($sh in $sld.Shapes) {
    $isTable = $false
    try { $isTable = [bool]$sh.HasTable } catch {}
    if ($isTable) {
      $tb = $sh.Table
      for ($r = 1; $r -le $tb.Rows.Count; $r++) { for ($c = 1; $c -le $tb.Columns.Count; $c++) {
        try { scan $tb.Cell($r, $c).Shape $sld.SlideIndex 'cell' } catch {}
      } }
    } else { scan $sh $sld.SlideIndex 'shape' }
  }
}
$pres.Close(); $app.Quit()
$json = $res | ConvertTo-Json -Depth 4 -Compress
[System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
