# vk anim roject
Скрипт, отсылающий сообщение VK, ждущий прочтения и многократно редактирующий его с заданной периодичностью.  
Можно посылать мультики из ascii-арта или эмоджей:

![](https://gist.github.com/codeleventh/a6b2ce4bf933c1689376ed0100111e85/raw/fa4d8b318ba80efb7215879030890fb2f14b269c/vkanim.gif)

## Использование
Для работы требуется [модуль vk api wrapper](https://github.com/dimka665) (установка — `pip install vk`), аккаунт в соцсети и  идентификатор приложения (получить можно [здесь](https://vk.com/editapp?act=create)).

Логин, пароль и идентификатор вводятся в начало скрипта, после чего его можно использовать из командной строки:  
`py vkanim.py id_пользователя пауза_между_кадрами входной_файл`

Например, `py vkanim.py 1 0.75 skinhands.json`

В качестве получателя также может выступать чат. Для этого нужно указать его id, сложенный с числом 2000000000.

Анимации хранятся как JSON, в проекте есть несколько примеров и template.txt, который можно редактировать.

## Known issues
1. Скрипт делает панический exit() сразу же, как только VK предлагает ввести капчу, что рано или поздно происходит.
Решение — не отсылать слишком длинных анимаций и выставлять разумную задержку между кадрами.  
2. Cкрипт не будет работать вовсе, если к аккаунту отправителя не был привязан номер телефона -— в таких случаях VK выдает капчу на каждое отосланное сообщение.

## Todo
✓ Доработка скрипта (некоторые настройки анимаций игнорируются)  
✓ Обработка некорректных или неполных входных данных  
✓ Обработка ошибок от сервера
✗ Возможность отправлять фотографии в сообщениях  
~~✗ Независимость от стороннего модуля~~