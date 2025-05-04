@echo off
echo [HandTrip 수집 시스템]

IF NOT EXIST .env (
    echo [WARNING] .env 파일이 없습니다.
    echo .env.example 파일을 참고해서 .env 파일을 만들어주세요.
    pause
    exit /b
)

set /p REGION=수집할 지역명을 입력하세요 (예: 도쿄, 교토, 오사카, 후쿠오카):
set /p DRYRUN=dry-run 모드로 실행하시겠습니까? (y/n):
set /p SKIP_DESC=설명 수집을 생략하시겠습니까? (y/n):

setlocal enabledelayedexpansion
set OPTIONS=

if /I "!DRYRUN!"=="y" (
    set OPTIONS=!OPTIONS! --dry-run
)

if /I "!SKIP_DESC!"=="y" (
    set OPTIONS=!OPTIONS! --skip-description
)

echo.
echo [실행 중] python main.py --region !REGION! !OPTIONS!
python main.py --region !REGION! !OPTIONS!

echo.
echo [DONE] 엔터를 눌러 종료합니다.
pause
