$ErrorActionPreference = 'Stop'

$files = @('src/pageHtml.ts', 'src/footerHtml.ts') + (Get-ChildItem 'references/original-html' -File | Select-Object -ExpandProperty FullName)
$tagPattern = '<img\b[^>]*?src=\\?"(?<url>https://lh3\.googleusercontent\.com[^"\\]+)\\?"[^>]*>'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$entries = [ordered]@{}
$usedNames = @{}

foreach ($file in $files) {
  $content = [System.IO.File]::ReadAllText((Resolve-Path $file), [System.Text.Encoding]::UTF8)
  foreach ($match in [regex]::Matches($content, $tagPattern, 'IgnoreCase')) {
    $url = $match.Groups['url'].Value
    if ($entries.Contains($url)) { continue }

    $alt = [regex]::Match($match.Value, 'alt=\\?"(?<alt>[^"\\]*)').Groups['alt'].Value
    if ($alt -match 'Technology$') { $local = '/assets/chinh-nhan-logo.png' }
    elseif ($alt -match '^Tiáº¿ng Viá»‡t$') { $local = '/assets/flags/vi.svg' }
    elseif ($alt -eq 'English') { $local = '/assets/flags/en.svg' }
    elseif ($alt -match 'DMCA') { $local = '/assets/chinh-nhan/dmca-protected' }
    elseif ($alt -match '^ÄÃ£ thÃ´ng') { $local = '/assets/chinh-nhan/bo-cong-thuong-notification' }
    # This single CDN object is access-restricted (HTTP 403); reuse the closest local camera-service photo.
    elseif ($url -match 'AEtjO1UlmR2P') { $local = '/assets/chinh-nhan/close-up-of-a-professional-technician-in-uniform-repairing.jpg' }
    else {
      $base = $alt.ToLowerInvariant() -replace '&amp;', 'and' -replace '[^a-z0-9]+', '-' -replace '(^-+|-+$)', ''
      if ([string]::IsNullOrWhiteSpace($base)) { $base = 'service-image' }
      if ($base.Length -gt 58) { $base = $base.Substring(0, 58).TrimEnd('-') }
      if ($usedNames.Contains($base)) { $usedNames[$base]++; $base = "$base-$($usedNames[$base])" } else { $usedNames[$base] = 1 }
      $local = "/assets/chinh-nhan/$base"
    }
    $entries[$url] = [pscustomobject]@{ local = $local; alt = $alt }
  }

  $backgroundIndex = 0
  foreach ($match in [regex]::Matches($content, '(?<url>https://lh3\.googleusercontent\.com[^"''\s\\]+)(?=&quot;|["''\s\\])', 'IgnoreCase')) {
    $url = $match.Groups['url'].Value
    if ($entries.Contains($url)) { continue }
    $backgroundIndex++
    $pageName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $entries[$url] = [pscustomobject]@{ local = "/assets/chinh-nhan/$pageName-background-$backgroundIndex"; alt = "$pageName background image" }
  }
}

New-Item -ItemType Directory -Force -Path 'public/assets/chinh-nhan' | Out-Null
$downloaded = 0
$failed = @()

foreach ($entry in $entries.GetEnumerator()) {
  if ($entry.Key -match 'AEtjO1UlmR2P') { continue }
  if ($entry.Value.local -notlike '/assets/chinh-nhan/*') { continue }
  $basePath = Join-Path $PWD ('public' + $entry.Value.local)
  $temporaryPath = "$basePath.download"
  try {
    Invoke-WebRequest -Uri $entry.Key -OutFile $temporaryPath -TimeoutSec 30
    $bytes = [System.IO.File]::ReadAllBytes($temporaryPath)
    if ($bytes.Length -lt 100) { throw "Downloaded content is unexpectedly small ($($bytes.Length) bytes)." }
    $extension = if ($bytes[0] -eq 0xFF -and $bytes[1] -eq 0xD8) { '.jpg' } elseif ($bytes[0] -eq 0x89 -and $bytes[1] -eq 0x50) { '.png' } elseif ($bytes[0] -eq 0x52 -and $bytes[1] -eq 0x49 -and $bytes[8] -eq 0x57) { '.webp' } elseif ($bytes[0] -eq 0x47 -and $bytes[1] -eq 0x49) { '.gif' } else { '.img' }
    Move-Item -Force -LiteralPath $temporaryPath -Destination ($basePath + $extension)
    $entry.Value.local = $entry.Value.local + $extension
    $downloaded++
  } catch {
    if (Test-Path -LiteralPath $temporaryPath) { Remove-Item -LiteralPath $temporaryPath -Force }
    # Preserve offline rendering if a protected remote asset cannot be retrieved.
    $entry.Value.local = '/assets/chinh-nhan/friendly-it-consultant.jpg'
    $failed += $entry.Value.alt
  }
}

if ($failed.Count -gt 0) {
  Write-Warning "Used the local fallback image for $($failed.Count) protected CDN asset(s): $($failed -join ', ')."
}

foreach ($file in $files) {
  $content = [System.IO.File]::ReadAllText((Resolve-Path $file), [System.Text.Encoding]::UTF8)
  foreach ($entry in $entries.GetEnumerator()) { $content = $content.Replace($entry.Key, $entry.Value.local) }
  [System.IO.File]::WriteAllText((Resolve-Path $file), $content, $utf8NoBom)
}

"Downloaded: $downloaded; mapped URLs: $($entries.Count)"
