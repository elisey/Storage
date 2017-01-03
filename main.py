import DataBase
from prettytable import PrettyTable
import argparse


def searchCommand(args):
    if args[0] == '-s':
        if args[1] is not None:
            #просмотреть все элементы в хранилище storageId
            try:
                storageId = int(args[1])
            except TypeError:
                print("wrong usage")
                return

            print("Элементы в хранилище ", str(storageId))
            items = DataBase.getItemsInStorage(storageId)

            t = PrettyTable( ['ID', 'Наименование', 'Кол-во'] )
            t.align = 'l'
            for item in items:
                if item is not None:
                    t.add_row([item[0], item[1], item[2]])
            print(t)

    elif args[0] == '-i':
        if args[1] is not None:
            #просмотреть все хранилища с элементом <itemId>
            try:
                itemId = int(args[1])
            except TypeError:
                print("wrong usage")
                return

            print("Хранилища с элементом ", str(itemId))
            items = DataBase.getStoragesOfItem(itemId)

            t = PrettyTable( ['ID', 'Наименование хранилища', 'Кол-во'] )
            t.align = 'l'

            for item in items:
                if item is not None:
                    t.add_row([item[0], item[1], item[2]])
            print(t)

    else:
        if args[0] is not None:
            #получить все элементы, в названии которых содержится args[1]
            seatchString = args[0]
            print('Поиск элементов по фразе "', seatchString, '"')
            items = DataBase.getItems(seatchString)

            t = PrettyTable(['ID', 'Наименование', 'Кол-во'])
            t.align = 'l'

            for item in items:
                if item is not None:
                    t.add_row([item[0][0], item[0][1], item[1]])
            print(t)

def main():
    while True:
        args = input('>').split()
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
        parser_storage.add_argument('--parentid', '-p', dest='parent', type=int)
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

        print(parser.parse_args(args))


if __name__ == '__main__':
    main()