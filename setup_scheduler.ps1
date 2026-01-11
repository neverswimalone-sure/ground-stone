# 골프 딜 뉴스 봇 - 윈도우 작업 스케줄러 자동 설정 스크립트
# 관리자 권한으로 실행해야 합니다

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  골프 딜 뉴스 봇 - 작업 스케줄러 설정" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 현재 스크립트 위치
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatFilePath = Join-Path $ScriptPath "run_golf_bot.bat"

Write-Host "현재 경로: $ScriptPath" -ForegroundColor Yellow
Write-Host ""

# 관리자 권한 체크
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ 오류: 이 스크립트는 관리자 권한으로 실행해야 합니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "해결 방법:" -ForegroundColor Yellow
    Write-Host "1. PowerShell을 관리자 권한으로 실행" -ForegroundColor White
    Write-Host "2. 이 스크립트가 있는 폴더로 이동" -ForegroundColor White
    Write-Host "3. .\setup_scheduler.ps1 명령어 실행" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

# Python 경로 확인
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "❌ Python이 설치되어 있지 않거나 PATH에 등록되어 있지 않습니다." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✅ Python 경로: $pythonPath" -ForegroundColor Green

# 작업 스케줄러 설정
$TaskName = "GolfDealNewsBot"
$TaskDescription = "골프장 투자 및 M&A 뉴스를 수집해서 텔레그램으로 전송 (평일 9-18시, 30분 간격)"

# 기존 작업이 있으면 삭제
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  기존 작업을 삭제합니다..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# 작업 생성
Write-Host "📅 작업 스케줄러에 등록 중..." -ForegroundColor Cyan

# 액션 정의
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"cd /d `"$ScriptPath`" && run_golf_bot.bat`"" -WorkingDirectory $ScriptPath

# 트리거 정의 (평일 오전 9시 시작, 30분마다 반복, 9시간 동안)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 9:00AM

# 반복 설정 (30분마다, 9시간 동안)
$trigger.Repetition = (New-ScheduledTaskTrigger -Once -At 9:00AM -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Hours 9)).Repetition

# 설정
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

# 작업 등록
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $TaskDescription `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Limited

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  ✅ 작업 스케줄러 등록 완료!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 설정 내용:" -ForegroundColor Cyan
Write-Host "  - 작업 이름: $TaskName" -ForegroundColor White
Write-Host "  - 실행 시간: 평일 (월~금) 오전 9시 ~ 오후 6시" -ForegroundColor White
Write-Host "  - 실행 간격: 30분마다" -ForegroundColor White
Write-Host "  - 파일 경로: $BatFilePath" -ForegroundColor White
Write-Host ""
Write-Host "💡 확인 방법:" -ForegroundColor Yellow
Write-Host "  1. 작업 스케줄러 열기 (taskschd.msc)" -ForegroundColor White
Write-Host "  2. 왼쪽 메뉴에서 '작업 스케줄러 라이브러리' 선택" -ForegroundColor White
Write-Host "  3. '$TaskName' 작업 확인" -ForegroundColor White
Write-Host ""
Write-Host "🔧 수정/삭제 방법:" -ForegroundColor Yellow
Write-Host "  - 작업 스케줄러에서 직접 수정 가능" -ForegroundColor White
Write-Host "  - 또는 이 스크립트를 다시 실행하면 재설정됨" -ForegroundColor White
Write-Host ""
pause
