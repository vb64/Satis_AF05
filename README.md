# Пример использования анализатора спектра Satis AF-05 в Python
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/Satis_AF05/satis%20pep257?label=Pep257&style=plastic)](https://github.com/vb64/Satis_AF05/actions?query=workflow%3A%22satis+pep257%22)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/Satis_AF05/satis%20tests?label=Python%203.6%203.7%203.8%203.9%203.10&style=plastic)](https://github.com/vb64/Satis_AF05/actions?query=workflow%3A%22satis+tests%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/df385d9214b94778b22c630c7d4baefa)](https://www.codacy.com/gh/vb64/Satis_AF05/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/Satis_AF05&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/df385d9214b94778b22c630c7d4baefa)](https://www.codacy.com/gh/vb64/Satis_AF05/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/Satis_AF05&utm_campaign=Badge_Coverage)

Данный пример реализует взаимодействие с анализатором спектра Satis AF-05 в языке программирования Python.
Вы можете использовать готовый исполняемый файл [satis.exe](https://github.com/vb64/Satis_AF05/releases/tag/ver.1.0) или [собрать собственную версию](https://github.com/vb64/Satis_AF05/tree/readme#%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0-%D1%81%D0%BE%D0%B1%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D0%B9-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D0%B5%D0%BC%D0%BE%D0%B3%D0%BE-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-%D0%B8%D0%B7-%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D1%8B%D1%85-%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2) исполняемого файла из исходных кодов.

[![Satis AF-05](/img/device.jpg)](http://www.satis-tl.ru/products/oborudovanie-sistem-upravleniya-i-kontrolya-setey-sputnikovoy-svyazi/analizator-chastotnyy-af-4/)

## Подключение Satis AF-05 к компьютеру

Перед началом работы необходимо подключить анализатор к компьютеру, на котором будет запускаться программа примера.
Нужно соединить кабелем Ethernet анализатор и компьютер напрямую либо через коммутатор.
По умолчанию у анализатора установлен IP адрес 192.168.0.100. Сетевую карту компьютера, соединенную с анализатором, нужно настроить на работу в данной подсети.

Если настройки сделаны правильно и соединение работает, при открытии в браузере адреса 192.168.0.100 вы должны увидеть что-то похожее на следующую картинку.

![Веб-интерфейс](/img/browser.jpg)

## Считывание данных анализатора

Пример реализует два режима работы с анализатором - чтение данных сигнала в заданном диапазоне частот и режим чтения данных для заданной частоты.

### Команда 'read'

Команда 'read' реализует режим чтения данных в заданном диапазоне частот с заданными параметрами.

```bash
satis.exe read --address=192.168.1.100 --freq_start=1400000000 --freq_end=1400330000 --video=50 --rbw=0 --atten=0 --with_data
```

В данном режиме программа принимает следующие параметры

-   --addres строка адреса, по которому доступен анализатор. по умолчанию '192.168.0.100'
-   --freq_start начальная частота диапазона в герцах. допустимые значения от 950000000 до 2150000000. по умолчанию 950000000.
-   --freq_end конечная частота диапазона в герцах. допустимые значения от 950000000 до 2150000000. по умолчанию 2150000000.
-   --video частота усреднения результата на периоде времени в герцах. допустимые значения от 0.1 (период 10 секунд) до 6400 (период 0.156 миллисекунды). по умолчанию 100.
-   --rbw разрешение по частоте. целое число от 0 до 4. по умолчанию 2 (400 Гц).
    - 0: 6400 Гц
    - 1: 1600 Гц
    - 2: 400 Гц
    - 3: 100 Гц
    - 4: 25 Гц
-   --atten аттенюация входного сигнала. целое число от 0 до 6. по умолчанию 0 (0 дБ).
    - 0: 0 дБ
    - 1: 5 дБ
    - 2: 10 дБ
    - 3: 16 дБ
    - 4: 21 дБ
    - 5: 26 дБ
    - 6: 31 дБ
-   --with_data вывод на экран значений прочитанных данных. по умолчанию выводится только размер массива считанных данных.

В процессе работы команда выводит на экран данные, получаемые от анализатора. По завершении цикла чтения данных выводится общее количество считанных значений сигнала.

### Команда 'sweep'

Команду 'sweep' можно использовать в ситуации, когда вас интересует значение сигнала на заранее известной вам частоте.
Команда максимально быстро выведет список значений сигнала в окрестностях заданной частоты.

```bash
satis.exe sweep --address=192.168.1.100 --freq_center=1450000000 --datafreq=10 --rbwsweep=0 --atten=0
```

В данном режиме программа принимает следующие параметры

-   --freq_center интересующая частота в Гц. от 950000000 до 2150000000. по умолчанию 950000000.
-   --datafreq период осреднения в Гц. от 1.0 до 20.0. по умолчанию 10.
-   --rbwsweep разрешение по частоте. целое число от 0 до 2. по умолчанию 0 (6400 Гц).
    - 0: 6400 Гц
    - 1: 1600 Гц
    - 2: 400 Гц

Остальные параметры имеют то же значение, что и в команде 'read'.

Команда выведет на экран данные, полученные от анализатора.

## Сборка собственной версии исполняемого файла из исходных кодов

Перечень средств разработки, необходимых для сборки исполняемого файла. Скачать и установить:

-   [Python 3](https://www.python.org/downloads/release/python-3810/)
-   [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов
-   GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций с makefile

Затем

```bash
git clone git@github.com:vb64/Satis_AF05.git
cd Satis_AF05
make setup PYTHON_BIN=/path/to/python3.exe
make tests
make exe
```

Файл `satis.exe` будет создан в каталоге `dist`.
