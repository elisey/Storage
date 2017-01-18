import DataBase
from prettytable import PrettyTable
import argparse


def searchItems(searchString):
    print('Поиск всех элементов"', searchString, '"')
    items = DataBase.searchItems(searchString)

    t = PrettyTable(['ID', 'Наименование', 'Кол-во'])
    t.align = 'l'

    for item in items:
        if item is not None:
            t.add_row([item[0], item[1], item[2]])
    print(t)

def storageAdd(storageName, parentId):
    status = DataBase.addStorage(storageName, parentId)
    parentName, result = DataBase.getStorageNameById(parentId)
    if status is True:
        print("Хранилище", storageName, "успешно добавлено в базу. Родитель:", parentName, '('+str(parentId)+')')
    else:
        print("Ошибка. Хранилище", storageName, "не добавлено в базу. Возможно указанный родитель не найден")

def storageViewById(storageId):
    storageName, result = DataBase.getStorageNameById(storageId)
    if result == False:
        print("Ошибка. Хранилище", storageId, "не найдено")
        return

    print("Элементы в хранилище", storageName, '('+str(storageId)+')')
    items = DataBase.getItemsInStorage(storageId)

    t = PrettyTable(['ID', 'Наименование', 'Кол-во'])
    t.align = 'l'
    for item in items:
        if item is not None:
            t.add_row([item[0], item[1], item[2]])
    print(t)

def itemView(itemId, itemName):
    if itemId is not None:
        itemName, result = DataBase.getItemNameById(itemId)
        if result == False:
            print("Ошибка. Элемент", itemId, "не найден")
            return
    else:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result == False:
            print("Ошибка. Элемент", itemName, "не найден")
            return

    print("Просмотр элемента", itemName, '(' + str(itemId) + ')')
    items = DataBase.getStoragesOfItem(itemId)

    t = PrettyTable(['ID', 'Наименование хранилища', 'Кол-во'])
    t.align = 'l'

    for item in items:
        if item is not None:
            t.add_row([item[0], item[1], item[2]])
    print(t)

def itemCreate(itemName, storageId, quantity):
    status = DataBase.createNewItem(itemName)

    if status is False:
        print("Ошибка. Элемент ", itemName, "не создан. Возможно элемент с таким именем уже существует")
        return

    itemId, result = DataBase.getItemIdByName(itemName)
    if result is True:
        print("Элемент ", itemName, '('+str(itemId)+')', "успешно создан")
    else:
        print("Неизвестная ошибка. Элемент ", itemName, "не создан")
        return

    if storageId is not None and quantity is not None:
        itemAdd(None, itemId, storageId, quantity)

#TODO Проверка существования элемента
def itemAdd(itemName = None, itemId = None, storageId = None, quantity = 0):
    if quantity == 0:
        print("Ошибка при добавлении элемента. Количество элементов должно быть больше ноля")
        return

    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при добавлении элемента")
            return

    DataBase.addItems(itemId, storageId, quantity)
    print("Элементы успешно добавлены")

def itemRemove(itemName = None, itemId = None, storageId = None, quantity = 0):
    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return

    result = DataBase.removeItems(itemId, storageId, quantity)

    if result == False:
        print("Ошибка при удалении элемента. Возможно указано некорректное количество элементов для удаления")
        return

    print("Элементы успешно удалены")
    return

def itemMove(itemName = None, itemId = None, storageIdSrc = None, storageIdDst = None, quantity = 0):
    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return

    result = DataBase.moveItems(itemId, storageIdSrc, storageIdDst, quantity)

    if result == False:
        print("Ошибка при перемещении элемента. Возможно указано некорректное количество элементов для перемещения")
        return

    print("Элементы успешно перемещены")
    return

def drawStoragesTreeById(storageId):
    currentStorageId = storageId
    while True:
        storageName, result = DataBase.getStorageNameById(currentStorageId)
        if result is False:
            return
        print(currentStorageId, '\t', storageName)
        currentStorageId, result = DataBase.getStorageParentId(currentStorageId)
        if currentStorageId == 0 or result is False:
            return

def main():
    while True:
        inputString = input('>').split()
        #print(args)

        parser = argparse.ArgumentParser(prog='PROG')
        #parser.add_argument('--foo', action='store_true', help='foo help')
        subparsers = parser.add_subparsers(help='sub-command help')

        #PARSER SEARCH
        parser_search = subparsers.add_parser('search', help='search help')
        parser_search.add_argument('search', action='store_true')
        parser_search.add_argument('--name', '-n', dest='name', type=str, nargs='*', help='name help')

        #PARSER STORAGE
        parser_storage = subparsers.add_parser('storage', help='storage help')
        parser_storage.add_argument('storage', action='store_true')
        parser_storage.add_argument('--add', '-a', action='store_true')
        parser_storage.add_argument('--view', '-v', action='store_true')

        parser_storage.add_argument('--name', '-n', dest='name', type=str, nargs='*')
        parser_storage.add_argument('--parentid', '-p', dest='parentid', type=int)
        parser_storage.add_argument('--id', '-i', dest='id', type=int)

        #PARSER ITEM
        parser_item = subparsers.add_parser('item', help='item help')
        parser_item.add_argument('item', action='store_true')
        parser_item.add_argument('--view', '-v', action='store_true')
        parser_item.add_argument('--create', '-c', action='store_true')
        parser_item.add_argument('--add', '-a', action='store_true')
        parser_item.add_argument('--remove', '-r', action='store_true')
        parser_item.add_argument('--move', '-m', action='store_true')

        parser_item.add_argument('--name', '-n', dest='name', type=str, nargs='*')
        parser_item.add_argument('--id', '-i', dest='id', type=int)
        parser_item.add_argument('--storageid', dest='storageId', type=int)
        parser_item.add_argument('--storageidsrc', dest='storageIdSrc', type=int)
        parser_item.add_argument('--storageiddst', dest='storageIdDst', type=int)
        parser_item.add_argument('--quantity', '-q', dest='quantity', type=int)

        #PARSER TREE
        parser_tree = subparsers.add_parser('tree', help='tree help')
        parser_tree.add_argument('tree', action='store_true')
        parser_tree.add_argument('--id', '-i', dest='id', type=int)

        #PARSER STATUS
        parser_status = subparsers.add_parser('status', help='status help')
        parser_status.add_argument('status', action='store_true')


        args = parser.parse_args(inputString)
        print(args)
        str2 = ' '
        if hasattr(args, "name") is True:
            if args.name is not None:
                args.name = str2.join(args.name)

        if hasattr(args, "search") is True:
            if args.name is not None:
                searchItems(args.name)
            else:
                print("Ошибка. Не указана строка для поиска (--name)")

        elif hasattr(args, "storage") is True:
            if args.add == True:
                if args.name is not None and args.parentid is not None:
                    storageAdd(args.name, args.parentid)
                else:
                    print("Ошибка. Не указано имя или ID нового хранилища (--name or --parentid)")
            elif args.view == True:
                if args.id is not None:
                    storageViewById(args.id)
                else:
                    print("Ошибка. Не указано ID хранилища (--id)")
        elif hasattr(args, "item") is True:
            if args.view == True:
                if args.name is not None:
                    itemView(None, args.name)
                elif args.id is not None:
                    itemView(args.id, None)
                else:
                    print("Ошибка. Не указан элемент (--name or --id)")
            elif args.create == True:
                if args.name is not None:
                    itemCreate(args.name, args.storageId, args.quantity)
                else:
                    print("Ошибка. Не указано имя нового элемента (--name)")
            elif args.add == True:
                if args.name is None and args.id is None:
                    print("Ошибка. Не указан элемент (--name or --id)")
                    continue
                if args.storageId is None:
                    print("Ошибка. Не указан ID хранилища (--storageid)")
                    continue
                if args.quantity is None:
                    print("Ошибка. Не указано количество элементов (--quantity)")
                    continue
                itemAdd(args.name, args.id, args.storageId, args.quantity)
            elif args.remove == True:
                if args.name is None and args.id is None:
                    print("Ошибка. Не указан элемент (--name or --id)")
                    continue
                if args.storageId is None:
                    print("Ошибка. Не указан ID хранилища (--storageid)")
                    continue
                if args.quantity is None:
                    print("Ошибка. Не указано количество элементов (--quantity)")
                    continue
                itemRemove(args.name, args.id, args.storageId, args.quantity)
            elif args.move == True:
                if args.name is None and args.id is None:
                    print("Ошибка. Не указан элемент (--name or --id)")
                    continue
                if args.storageIdSrc is None:
                    print("Ошибка. Не указан ID исходного хранилища (--storageidsrc)")
                    continue
                if args.storageNameDst is None and args.storageIdDst is None:
                    print("Ошибка. Не указан ID конечного хранилища (--storageiddst)")
                    continue
                if args.quantity is None:
                    print("Ошибка. Не указано количество элементов (--quantity)")
                    continue
                itemMove(args.name, args.id, args.storageIdSrc, args.storageIdDst, args.quantity)

        elif hasattr(args, "tree") is True:
            if args.id is not None:
                drawStoragesTreeById(args.id)
            else:
                print("Ошибка. Не указан ID хранилища (--id)")




if __name__ == '__main__':
    main()