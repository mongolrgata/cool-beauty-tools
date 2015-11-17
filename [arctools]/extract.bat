rem Извлечение файлов из всех архивов в текущей директории
for %%A in (*.arc) do python arctools.py extract %%A
pause
