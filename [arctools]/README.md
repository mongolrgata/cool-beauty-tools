## arctools

Работа с **\*.arc**-архивом, извлечение и упаковка файлов.

## Использование

-   Извлечение файлов из архива (файлы будут извлечены в одноименную папку)

    ```
    arctools.py extract (<arc_filename>)
    ```

    Дополнительно будет создан **order**-файл, в котором будут перечислены имена извлечённых файлов:

    ```
    .\archive.arc

    .\archive\file1.ext
    .\archive\file2.ext
     ...
    .\archive\fileN.ext
    .\archive\order
    ```

-   Упаковка файлов в архив

    ```
    arctools.py pack (<directory>)
    ```
