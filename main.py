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
    print("Adding new item")

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
        parser_search.add_argument('--name', '-n', dest='name', type=str, help='name help')

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
        parser_item.add_argument('--storagename', dest='storagename', type=str)
        parser_item.add_argument('--storageid', dest='storageid', type=int)
        parser_item.add_argument('--storagenamesrc', dest='storagenamesrc', type=str)
        parser_item.add_argument('--storageidsrc', dest='storageidsrc', type=int)
        parser_item.add_argument('--storagenamedst', dest='storagenamedst', type=str)
        parser_item.add_argument('--storageiddst', dest='storageiddst', type=int)
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
            elif args.create is not None:
                if args.name is not None:
                    itemCreate(args.name)
            elif args.add is not None:
                if (args.name is not None or args.id is not None) and (args.storageName is not None or args.storageId is not None) and (args.quantity is not None):
                    itemAdd(args.name, args.id, args.storageName, args.storageId, args.quantity)



if __name__ == '__main__':
    main()