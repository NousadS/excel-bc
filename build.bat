mkdir build
copy src\icon.ico build\icon.ico
pyinstaller ./src/main.py --noconfirm --log-level=WARN --clean --distpath="./build/" --workpath="./build/cache" --specpath="./build/" --onefile --name="EXCEL" --optimize=2 --noconsole --icon=icon.ico --add-data="icon.ico;."