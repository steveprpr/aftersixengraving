<# 
.SYNOPSIS
  Extract zips (optional) and copy ONLY .svg files found anywhere under Root
  into a top-level 'SVG' folder, auto-renaming on collisions.

.USAGE
  .\Collect-SVGs.ps1
  .\Collect-SVGs.ps1 -Root "C:\Path\To\Folder"
  .\Collect-SVGs.ps1 -SkipZipExtraction
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$Root = (Get-Location).Path,

    [switch]$SkipZipExtraction
)

# Zip support (for Windows PowerShell 5.1)
try { Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop } catch {}

function Get-UniqueFileDestination {
    param(
        [Parameter(Mandatory=$true)][string]$DestinationFolder,
        [Parameter(Mandatory=$true)][string]$FileName
    )
    $target = Join-Path $DestinationFolder $FileName
    if (-not (Test-Path -LiteralPath $target)) { return $target }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    $ext  = [System.IO.Path]::GetExtension($FileName)

    $i = 1
    do {
        $candidate = Join-Path $DestinationFolder ("{0}_{1}{2}" -f $base, $i, $ext)
        $i++
    } while (Test-Path -LiteralPath $candidate)
    return $candidate
}

function Get-UniquePath {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $Path }
    $dir = [System.IO.Path]::GetDirectoryName($Path)
    $name = [System.IO.Path]::GetFileName($Path)
    $i = 1
    do {
        $candidate = Join-Path $dir ("{0}_{1}" -f $name, $i)
        $i++
    } while (Test-Path -LiteralPath $candidate)
    return $candidate
}

Write-Host "Root directory: $Root" -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath $Root)) { throw "Root directory does not exist: $Root" }

# Create / reuse destination
$svgFolder = Join-Path $Root "SVG"
if (-not (Test-Path -LiteralPath $svgFolder)) {
    New-Item -ItemType Directory -Path $svgFolder | Out-Null
    Write-Host "Created folder: $svgFolder" -ForegroundColor Green
} else {
    Write-Host "Using existing folder: $svgFolder" -ForegroundColor Yellow
}

# 1) Optional: extract ZIPs at the root
$zipsExtracted = 0
if (-not $SkipZipExtraction) {
    $zipFiles = Get-ChildItem -LiteralPath $Root -Filter *.zip -File | Sort-Object Name
    foreach ($zip in $zipFiles) {
        try {
            $extractBase = [System.IO.Path]::GetFileNameWithoutExtension($zip.Name)
            $extractDir  = Get-UniquePath -Path (Join-Path $Root $extractBase)
            Write-Host "`nExtracting: $($zip.Name) -> $extractDir" -ForegroundColor Cyan
            [System.IO.Compression.ZipFile]::ExtractToDirectory($zip.FullName, $extractDir)
            $zipsExtracted++
        } catch {
            Write-Warning "Failed to extract '$($zip.FullName)': $($_.Exception.Message)"
        }
    }
}

# 2) Find ONLY .svg files anywhere under Root, excluding the SVG folder itself
Write-Host "`nScanning for .svg files under: $Root" -ForegroundColor Cyan

# Use -Filter (case-insensitive) and wildcard path so filtering happens in the provider, not post-hoc
$searchPath = (Join-Path $Root '*')
$allSVGs = Get-ChildItem -Path $searchPath -Recurse -Filter *.svg -File -ErrorAction SilentlyContinue |
           Where-Object { $_.FullName -notlike "$svgFolder*" }

$foundCount = ($allSVGs | Measure-Object).Count
$copiedCount = 0

foreach ($svg in $allSVGs) {
    try {
        $dest = Get-UniqueFileDestination -DestinationFolder $svgFolder -FileName $svg.Name
        Copy-Item -LiteralPath $svg.FullName -Destination $dest
        $copiedCount++
        Write-Host "Copied: $($svg.FullName) -> $dest" -ForegroundColor Green
    } catch {
        Write-Warning "Failed to copy '$($svg.FullName)': $($_.Exception.Message)"
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Magenta
if (-not $SkipZipExtraction) { Write-Host "ZIPs extracted : $zipsExtracted" }
Write-Host "SVGs found     : $foundCount"
Write-Host "SVGs copied    : $copiedCount"
Write-Host "SVG folder     : $svgFolder"
