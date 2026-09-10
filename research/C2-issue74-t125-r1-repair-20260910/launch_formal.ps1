param(
  [Parameter(Mandatory=$true)][string]$Trigger,
  [Parameter(Mandatory=$true)][string]$Python,
  [Parameter(Mandatory=$true)][string]$Program,
  [Parameter(Mandatory=$true)][string]$Meta,
  [Parameter(Mandatory=$true)][string]$U,
  [Parameter(Mandatory=$true)][string]$V,
  [Parameter(Mandatory=$true)][string]$W,
  [Parameter(Mandatory=$true)][string]$Output,
  [Parameter(Mandatory=$true)][string]$DeadlineUtc
)
$ErrorActionPreference = 'Stop'
$env:OMP_NUM_THREADS = '2'
$env:OPENBLAS_NUM_THREADS = '2'
$env:MKL_NUM_THREADS = '2'
$env:CUDA_VISIBLE_DEVICES = '-1'
$deadline = [DateTimeOffset]::Parse($DeadlineUtc)
while (-not (Test-Path -LiteralPath $Trigger)) {
  if ([DateTimeOffset]::UtcNow -ge $deadline) { exit 124 }
  Start-Sleep -Milliseconds 200
}
$dir = Split-Path -Parent $Output
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$stdout = Join-Path $dir 'stdout.log'
$stderr = Join-Path $dir 'stderr.log'
$arguments = @($Program, '--meta', $Meta, '--u', $U, '--v', $V, '--w', $W, '--output', $Output)
$process = Start-Process -FilePath $Python -ArgumentList $arguments -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$process.ProcessorAffinity = [IntPtr]3
$limit = 8GB
$breach = $null
while (-not $process.HasExited) {
  $process.Refresh()
  if ($process.WorkingSet64 -gt $limit) { $breach = 'memory'; Stop-Process -Id $process.Id -Force; break }
  if ([DateTimeOffset]::UtcNow -ge $deadline) { $breach = 'deadline'; Stop-Process -Id $process.Id -Force; break }
  Start-Sleep -Milliseconds 200
}
$process.WaitForExit()
$record = [ordered]@{ launcher_pid=$PID; formal_pid=$process.Id; exit_code=$process.ExitCode; breach=$breach; finished_utc=[DateTimeOffset]::UtcNow.ToString('o'); cpu_affinity='0x3'; memory_limit_bytes=$limit; gpu_used=$false }
$record | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dir 'supervisor.json') -Encoding utf8
exit $process.ExitCode
