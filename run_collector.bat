@echo off
set /p REGION=수집할 지역명을 입력하세요 (예: 도쿄, 교토, 오사카, 후쿠오카):

echo.
echo [INFO] 선택한 지역: %REGION%
python main.py --region %REGION%

pause
