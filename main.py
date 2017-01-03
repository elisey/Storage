import DataBase
from prettytable import PrettyTable

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
        print(args)
        if args[0] == 'search':
            searchCommand(args[1:])



if __name__ == '__main__':
    main()