## Команды

### Поиск
search -name STRING - получить все элементы, в названии которых содержится STRING

### Работа с хранилищами
storage --add --name STRING --parent INT - добавить хранилище с именем STRING и родителем INT
storage --view --name STRING - просмотреть содержание хранилища с именем STRING
storage --view --id INT - просмотреть содержание хранилища с ID INT

### Работа с элементами
item --view --name STRING - просмотреть наличие элемента с именем STRING в хранилищах
item --view --id INT - просмотреть наличие элемента с ID INT в хранилищах

item --create STRING
item --add --name STRING1 --id INT1 --storagename STRING1 --storageid INT2 -quantity INT3
item --remove --name STRING1 --id INT1 --storagename STRING2 --storageid INT2 -quantity INT3
item --move --name STRING1 --id INT1 --storagenamesrc STRING2 --storageidsrc INT2 --storagenamedst STRING3 --storageiddst INT3 -quantity INT4

### Работа с деревом хранилищ
tree - построить дерево хранилищ
tree --storagename STRING1 --storageid INT2 - построить дерево для хранилища

### Вспомогательные функции
--status - общая информация
--help - справка
--version

## TODO

### В модуль работы с БД
 - Получить имя элемента по его ID
 - Получить имя хранлища по его ID
 - Получить ID хранилища по его имени
 - Добавление хранилища
 
### Основная логика приложения
 - Отображение дерева хранилищ
 - Вывод основного статуса программы
 - При добавлении элемента возможность сразу добавить нужное количество элементов в заданное хранилище
 - После успешного добавления элемента отображать ID этого элемента