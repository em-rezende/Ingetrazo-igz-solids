# =========================================================================
# Copyright (C) 2026 Ezequiel M. Rezende
# License: GPL-3.0-or-later (same as IngeTrazo)
# =========================================================================
# Build the distributable igz_solids.zip for the IngeTrazo extension
# catalog (https://github.com/ingelibre/ingetrazo-extensions).
#
# Windows / PowerShell builder — no Python needed. It produces the SAME
# archive layout as packaging/build_extension.py (one top-level folder,
# igz_solids/, holding the code + tb_list.txt + i18n/ + icons/ + docs).
# That folder is what the catalog/IngeTrazo unpacks into <plugins>/, so the
# installed path becomes <plugins>/igz_solids/.
#
# The catalog installs ONE file per entry: a .py file, or a .zip holding a
# single folder with an __init__.py (see TEMPLATE.toml in that repository).
#
# Fixed entry timestamps keep the archive stable: rebuilding it prints the
# same SHA-256 as long as the content is unchanged. That SHA-256 is the
# value pasted into extensions/igz_solids.toml, and must match the file
# uploaded as the GitHub Release asset of the tag named in `download`.
#
# Usage:
#     powershell -ExecutionPolicy Bypass -File packaging\build_extension.ps1
#
# Output:
#     dist/igz_solids.zip
#     dist/igz_solids.zip.sha256
# =========================================================================
[CmdletBinding()]
param(
    [string]$Output
)

$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $Output) { $Output = Join-Path $scriptDir '..\dist' }

$root = (Resolve-Path (Join-Path $scriptDir '..')).Path
$package = 'igz_solids'
$zipName = "$package.zip"
$packageSrc = Join-Path $scriptDir $package

# Fixed timestamp -> reproducible archive.
$fixed = [System.DateTimeOffset]::new(2026, 1, 1, 0, 0, 0, [System.TimeSpan]::Zero)

$outDir = [System.IO.Path]::GetFullPath($Output)
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$zipPath = Join-Path $outDir $zipName
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }

# --- Collect the files, then sort by archive path --------------------------
$entries = New-Object System.Collections.Generic.List[object]

function Add-Entry([string]$arc, [string]$src) {
    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) { return }
    $entries.Add([pscustomobject]@{ Arc = $arc; Src = $src })
}

# The whole package tree (code, tb_list.txt, i18n/, LICENSE, THIRD-PARTY.md).
Get-ChildItem -LiteralPath $packageSrc -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\__pycache__\\' -and $_.Extension -notin @('.pyc', '.pyo') } |
    ForEach-Object {
        $rel = $_.FullName.Substring($packageSrc.Length + 1).Replace('\', '/')
        Add-Entry "$package/$rel" $_.FullName
    }

# Documentation kept at the repository root.
foreach ($f in @('README.md', 'README_ptBR.md')) {
    Add-Entry "$package/$f" (Join-Path $root $f)
}

# Icons from the repository root.
$iconsDir = Join-Path $root 'icons'
if (Test-Path -LiteralPath $iconsDir) {
    Get-ChildItem -LiteralPath $iconsDir -Filter '*.svg' |
        Sort-Object Name |
        ForEach-Object { Add-Entry "$package/icons/$($_.Name)" $_.FullName }
}

# De-duplicate by archive name (root docs may already live in the package).
$sorted = $entries | Sort-Object Arc -Unique

# --- Write the zip ---------------------------------------------------------
$stream = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::CreateNew)
try {
    $archive = New-Object System.IO.Compression.ZipArchive(
        $stream, [System.IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($e in $sorted) {
            $entry = $archive.CreateEntry(
                $e.Arc, [System.IO.Compression.CompressionLevel]::Optimal)
            $entry.LastWriteTime = $fixed
            $dest = $entry.Open()
            try {
                $bytes = [System.IO.File]::ReadAllBytes($e.Src)
                $dest.Write($bytes, 0, $bytes.Length)
            } finally {
                $dest.Dispose()
            }
        }
    } finally {
        $archive.Dispose()
    }
} finally {
    $stream.Dispose()
}

# --- SHA-256 ---------------------------------------------------------------
$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLower()
Set-Content -LiteralPath "$zipPath.sha256" -Value "$hash  $zipName" -Encoding ascii

$version = '0.0.0'
$readme = Join-Path $root 'README.md'
if (Test-Path -LiteralPath $readme) {
    foreach ($line in Get-Content -LiteralPath $readme) {
        if ($line -match '\*\*Version:\*\*\s*(\S+)') { $version = $Matches[1]; break }
    }
}

Write-Host "igz_solids $version"
Write-Host "  $zipPath"
Write-Host ("  sha256 = ""{0}""" -f $hash)
Write-Host ''
Write-Host '  Paste that sha256 into extensions/igz_solids.toml and upload'
Write-Host "  $zipName to the GitHub Release of the tag in ``download``."
