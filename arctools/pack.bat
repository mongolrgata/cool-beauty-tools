rem <Переупаковка> всех архивов в текущей директории
for %%A in (*.arc) do python arctools.py pack %%~nA
pause
