# Пример использования анализатора спектра Satis AF-05 в Python
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/Satis_AF05/satis%20pep257?label=Pep257&style=plastic)](https://github.com/vb64/Satis_AF05/actions?query=workflow%3A%22satis+pep257%22)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/Satis_AF05/satis%20tests?label=Python%203.6%203.7%203.8%203.9%203.10&style=plastic)](https://github.com/vb64/Satis_AF05/actions?query=workflow%3A%22satis+tests%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/df385d9214b94778b22c630c7d4baefa)](https://www.codacy.com/gh/vb64/Satis_AF05/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/Satis_AF05&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/df385d9214b94778b22c630c7d4baefa)](https://www.codacy.com/gh/vb64/Satis_AF05/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/Satis_AF05&utm_campaign=Badge_Coverage)

[![Satis AF-05](/img/device.jpg)](http://www.satis-tl.ru/products/oborudovanie-sistem-upravleniya-i-kontrolya-setey-sputnikovoy-svyazi/analizator-chastotnyy-af-4/)

## Подключение Satis AF-05 к компьютеру

![Веб-интерфейс](/img/browser.jpg)

## Считывание данных анализатора

### Команда 'read'

### Команда 'sweep'

## Сборка своей версии исполняемого файла из исходных кодов

Перечень средств разработки, необходимых для сборки дистрибутива. Скачать и установить:

- [Python 3](https://www.python.org/downloads/release/python-3810/)
- [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов
- GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций с makefile

Затем

```bash
git clone git@github.com:vb64/Satis_AF05.git
cd Satis_AF05
make setup PYTHON_BIN=/path/to/python3.exe
make tests
make exe
```

Файл `satis.exe` будет создан в каталоге `dist`.
