@echo off
rem Запуск с автоматической передачей тестовых путей к файлам VFS и скрипта
python src/main.py --vfs vfs.csv --script start_script.sh
pause
