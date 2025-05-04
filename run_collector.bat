@echo off
echo [HandTrip ���� �ý���]

IF NOT EXIST .env (
    echo [WARNING] .env ������ �����ϴ�.
    echo .env.example ������ �����ؼ� .env ������ ������ּ���.
    pause
    exit /b
)

set /p REGION=������ �������� �Է��ϼ��� (��: ����, ����, ����ī, �����ī):
set /p DRYRUN=dry-run ���� �����Ͻðڽ��ϱ�? (y/n):
set /p SKIP_DESC=���� ������ �����Ͻðڽ��ϱ�? (y/n):

setlocal enabledelayedexpansion
set OPTIONS=

if /I "!DRYRUN!"=="y" (
    set OPTIONS=!OPTIONS! --dry-run
)

if /I "!SKIP_DESC!"=="y" (
    set OPTIONS=!OPTIONS! --skip-description
)

echo.
echo [���� ��] python main.py --region !REGION! !OPTIONS!
python main.py --region !REGION! !OPTIONS!

echo.
echo [DONE] ���͸� ���� �����մϴ�.
pause
