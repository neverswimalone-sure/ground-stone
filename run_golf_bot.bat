@echo off
REM 골프 딜 뉴스 봇 실행 배치 파일
REM 이 파일은 작업 스케줄러에서 실행됩니다

cd /d "%~dp0"
python golf_deal_bot.py

REM 로그 파일에 실행 시간 기록 (선택사항)
echo [%date% %time%] Golf Deal Bot executed >> bot_execution_log.txt
