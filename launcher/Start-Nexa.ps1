
$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Users\Yash\Desktop\Java Project\Projects\Nexa\nexa"
$Port = 8081
$PostgresService = "postgresql-x64-18"
$ReadyUrl = "http://localhost:8081/login.html"
$AppUrl = "http://localhost:8081/dashboard.html"

try {
    Set-Location $ProjectRoot

    Write-Host "`n========== NEXA STARTUP ==========" -ForegroundColor Cyan

    # 1. Start PostgreSQL if required
    $DbService = Get-Service -Name $PostgresService

    if ($DbService.Status -ne "Running") {
        Start-Service -Name $PostgresService
        (Get-Service -Name $PostgresService).WaitForStatus(
            "Running",
            [TimeSpan]::FromSeconds(30)
        )
    }

    Write-Host "PostgreSQL is running." -ForegroundColor Green

    # 2. Start Spring Boot if required
    $ExistingServer = Get-NetTCPConnection `
        -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

    if (-not $ExistingServer) {
        Start-Process -FilePath "powershell.exe" `
            -ArgumentList @(
                "-NoExit",
                "-Command",
                "Set-Location '$ProjectRoot'; .\mvnw.cmd spring-boot:run"
            ) `
            -WorkingDirectory $ProjectRoot

        $Started = $false

        for ($i = 0; $i -lt 60; $i++) {
            Start-Sleep -Seconds 2
            try {
                $Response = Invoke-WebRequest `
                    -Uri $ReadyUrl -UseBasicParsing -TimeoutSec 2
                if ($Response.StatusCode -eq 200) {
                    $Started = $true
                    break
                }
            }
            catch {}
        }

        if (-not $Started) {
            throw "Backend did not start. Check the Spring Boot terminal."
        }
    }

    Write-Host "Nexa backend is ready." -ForegroundColor Green

    # 3. Open the dashboard; select and start video from there
    $Edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
    $Chrome = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"

    if (Test-Path $Edge) {
        Start-Process -FilePath $Edge -ArgumentList "--app=$AppUrl"
    }
    elseif (Test-Path $Chrome) {
        Start-Process -FilePath $Chrome -ArgumentList "--app=$AppUrl"
    }
    else {
        Start-Process $AppUrl
    }

    Write-Host "Nexa is ready. Select a video from the dashboard." -ForegroundColor Green
}
catch {
    Write-Host "`nNEXA STARTUP ERROR: $_" -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}
