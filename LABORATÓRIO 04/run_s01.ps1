Param(
  [string]$Language = "java",
  [int]$Top = 200,
  [int]$MinStars = 1000,
  [string]$Since = "2019-01-01"
)

$ErrorActionPreference = "Stop"

# Carrega .env e .env.example automaticamente se GITHUB_TOKEN não estiver setado
function Load-DotEnvFile {
  param([string]$Path)
  if (Test-Path $Path) {
    Get-Content -Path $Path | ForEach-Object {
      if ($_ -match "^\s*#") { return }
      if ($_ -match "^") { return }
      $parts = $_ -split "=",2
      if ($parts.Length -eq 2) {
        $key = $parts[0].Trim()
        $val = $parts[1].Trim()
        if (-not [string]::IsNullOrWhiteSpace($key) -and -not $env:$key) {
          $env:$key = $val
        }
      }
    }
  }
}

if (-not $env:GITHUB_TOKEN) {
  $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  Load-DotEnvFile (Join-Path $scriptDir ".env")
  if (-not $env:GITHUB_TOKEN) {
    Load-DotEnvFile (Join-Path $scriptDir ".env.example")
  }
}

if (-not $env:GITHUB_TOKEN) {
  Write-Error "GITHUB_TOKEN não definido. Configure em .env/.env.example ou exporte na sessão."
  exit 1
}

python "main.py" collect --language $Language --top $Top --min-stars $MinStars --since $Since
python "main.py" export
python "main.py" analyze
python "main.py" report
