rmdir .dist /S /Q
rmdir .build /S /Q

cd src

pyinstaller ^
--name=eta_regulator_board_admin_toolbox ^
--noconsole --icon=assets/favicon.ico ^
--paths ../.venv/Lib/site-packages ^
--hidden-import main.py ^
--add-data assets/favicon.ico;src/assets ^
--add-data assets/icon.png;src/assets ^
--distpath ../.dist ^
--workpath ../.build ^
bootstrapper.py
