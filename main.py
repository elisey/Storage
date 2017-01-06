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
        print("Хранилище", storageName, "успешно добавлено в базу. Родитель: ID", parentId, parentName)
    else:
        print("Ошибка. Хранилище", storageName, "не добавлено в базу. Возможно хранилище с таким именем уже существует или указанный родитель не найден")

def storageViewByName(storageName):
    storageId, result = DataBase.getStorageIdByName(storageName)

    if result == False:
        print("Ошибка. Хранилище", storageName, "не найдено")
        return
    storageViewById(storageId)

def storageViewById(storageId):
    print("Элементы в хранилище ", str(storageId))
    items = DataBase.getItemsInStorage(storageId)

    t = PrettyTable(['ID', 'Наименование', 'Кол-во'])
    t.align = 'l'
    for item in items:
        if item is not None:
            t.add_row([item[0], item[1], item[2]])
    print(t)

def itemViewByName(itemName):
    itemId, result = DataBase.getItemIdByName(itemName)

    if result == False:
        print("Ошибка. Элемент", itemName, "не найден")
        return
    itemViewById(itemId)

def itemViewById(itemId):
    print("Просмотр элемента", str(itemId))
    items = DataBase.getStoragesOfItem(itemId)

    t = PrettyTable(['ID', 'Наименование хранилища', 'Кол-во'])
    t.align = 'l'

    for item in items:
        if item is not None:
            t.add_row([item[0], item[1], item[2]])
    print(t)

def itemCreate(itemName):
    status = DataBase.createNewItem(itemName)
    if status is True:
        print("Элемент ", itemName, "успешно добавлен в базу")
    else:
        print("Ошибка. Элемент ", itemName, "не добавлен в базу. Возможно элемент с таким именем уже существует")

def itemAdd(itemName = None, itemId = None, storageName = None, storageId = None, quantity = 0):
    if quantity == 0:
        print("Ошибка при добавлении элемента. Количество элементов должно быть больше ноля")
        return

    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при добавлении элемента")
            return

    if storageId is None:
        storageId, result = DataBase.getStorageIdByName(storageName)
        if result is False:
            print("Неизвестная ошибка при добавлении элемента")
            return
    DataBase.addItems(itemId, storageId, quantity)
    print("Элементы успешно добавлены")

def itemRemove(itemName = None, itemId = None, storageName = None, storageId = None, quantity = 0):
    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return

    if storageId is None:
        storageId, result = DataBase.getStorageIdByName(storageName)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return
    result = DataBase.removeItems(itemId, storageId, quantity)

    if result == False:
        print("Ошибка при удалении элемента. Возможно указано некорректное количество элементов для удаления")
        return

    print("Элементы успешно удалены")
    return

def itemMove(itemName = None, itemId = None, storageNameSrc = None, storageIdSrc = None, storageNameDst = None, storageIdDst = None, quantity = 0):
    if itemId is None:
        itemId, result = DataBase.getItemIdByName(itemName)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return

    if storageIdSrc is None:
        storageIdSrc, result = DataBase.getStorageIdByName(storageNameSrc)
        if result is False:
            print("Неизвестная ошибка при удалении элемента")
            return

    if storageIdDst is None:
        storageIdDst, result = DataBase.getStorageIdByName(storageNameDst)
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

def drawStoragesTreeByName(storageName):
    storageId, result = DataBase.getStorageIdByName(storageName)

    if result is False:
        print("Ошибка. Хранилище с именем", storageName, "не найдено" )
        return
    drawStoragesTreeById(storageId)


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

        parser_storage.add_argument('--name', '-n', dest='name', type=str)
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

        parser_item.add_argument('--name', '-n', dest='name', type=str)
        parser_item.add_argument('--id', '-i', dest='id', type=int)
        parser_item.add_argument('--storagename', dest='storageName', type=str)
        parser_item.add_argument('--storageid', dest='storageId', type=int)
        parser_item.add_argument('--storagenamesrc', dest='storageNameSrc', type=str)
        parser_item.add_argument('--storageidsrc', dest='storageIdSrc', type=int)
        parser_item.add_argument('--storagenamedst', dest='storageNameDst', type=str)
        parser_item.add_argument('--storageiddst', dest='storageIdDst', type=int)
        parser_item.add_argument('--quantity', '-q', dest='quantity', type=int)

        #PARSER TREE
        parser_tree = subparsers.add_parser('tree', help='tree help')
        parser_tree.add_argument('tree', action='store_true')
        parser_tree.add_argument('--name', '-n', dest='name', type=str)
        parser_tree.add_argument('--id', '-i', dest='id', type=int)

        #PARSER STATUS
        parser_status = subparsers.add_parser('status', help='status help')
        parser_status.add_argument('status', action='store_true')


        args = parser.parse_args(inputString)
        print(args)


        if hasattr(args, "search") is True:
            searchItems(args.name)

        elif hasattr(args, "storage") is True:
            if args.add == True:
                if args.name is not None and args.parentid is not None:
                    storageAdd(args.name, args.parentid)
            elif args.view == True:
                if args.name is not None:
                    storageViewByName(args.name)
                elif args.id is not None:
                    storageViewById(args.id)

        elif hasattr(args, "item") is True:
            if args.view == True:
                if args.name is not None:
                    itemViewByName(args.name)
                elif args.id is not None:
                    itemViewById(args.id)
            elif args.create == True:
                if args.name is not None:
                    itemCreate(args.name)
            elif args.add == True:
                if (args.name is not None or args.id is not None) and (args.storageName is not None or args.storageId is not None) and (args.quantity is not None):
                    itemAdd(args.name, args.id, args.storageName, args.storageId, args.quantity)
            elif args.remove == True:
                if (args.name is not None or args.id is not None) and (args.storageName is not None or args.storageId is not None) and (args.quantity is not None):
                    itemRemove(args.name, args.id, args.storageName, args.storageId, args.quantity)
            elif args.move == True:
                if (args.name is not None or args.id is not None) and (args.storageNameSrc is not None or args.storageIdSrc is not None) and (args.storageNameDst is not None or args.storageIdDst is not None) and (args.quantity is not None):
                    itemMove(args.name, args.id, args.storageNameSrc, args.storageIdSrc, args.storageNameDst,args.storageIdDst, args.quantity)

        elif hasattr(args, "tree") is True:
            if args.id is not None:
                drawStoragesTreeById(args.id)
            if args.name is not None:
                drawStoragesTreeByName(args.name)




if __name__ == '__main__':
    main()