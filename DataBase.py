#!/usr/bin/env python
import sqlite3

DataBaseName = 'storageBase.db'

#Получить список (ID делати, название детали, количество деталей) для всех деталей, в названии которых содержится строка searchString
def searchItems(searchString):

    items = []
    foundItems = __searchItemsByName(searchString)
    for foundItem in foundItems:
        if foundItem is not None:
            numOfItems = __getNumOfItems(foundItem[0])
            items.append( (foundItem[0], foundItem[1], numOfItems,) )

    return items

#Получить список хранилищ с искомым элементом itemId (ID хранилища, название хранилища, количество деталей)
def getStoragesOfItem(itemId):

    items = []

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('SELECT ItemsAndStorages.storageId, storages.StorageName, ItemsAndStorages.Quantity  FROM itemsAndStorages, storages WHERE ItemId = ? AND storages.StorageId = ItemsAndStorages.StorageId', [str(itemId)])

    while True:
        item = c.fetchone()
        items.append(item)
        if item is None:
            break
    conn.close()
    return items

#Получить всех предков хранилища (Список ID текущего хранилища, название текущего хранилища, ID родителя)
def getStoragePath(storageId):
    storageList = []
    currentStorageId = storageId

    while currentStorageId is not 0:
        conn = sqlite3.connect(DataBaseName)
        c = conn.cursor()
        c.execute('SELECT ParrentStorageId, StorageName FROM storages WHERE StorageId = ?', [str(currentStorageId)])
        text = c.fetchone()
        conn.close()
        if text is None:
            break

        parrentStorageId = text[0]
        storageName = text[1]
        currentStorage = (currentStorageId, storageName, parrentStorageId, )
        storageList.append(currentStorage)

        currentStorageId = parrentStorageId

    return storageList

#Получить все детали в хранилище (список ID детали, название детали, количество деталей)
def getItemsInStorage(storageId):
    items = []

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT ItemsAndStorages.Itemid, items.ItemName, ItemsAndStorages.Quantity FROM ItemsAndStorages, items WHERE ItemsAndStorages.StorageId = ? AND items.ItemId = ItemsAndStorages.Itemid", [str(storageId)])

    while True:
        item = c.fetchone()
        items.append(item)
        if item is None:
            break
    conn.close()
    return items

#Проверить существует ли деталь с заданным названием
def isItemExist(itemName):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('SELECT COUNT(ItemId) FROM items WHERE ItemName=?', [itemName])
    text = c.fetchone()
    conn.close()

    if text[0] is 0:
        return False
    else:
        return True

#Попытаться вставить деталь с заданным названием, если она еще не существует
def createNewItem(newItemName):
    if isItemExist(newItemName) == True:
        return False
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("INSERT INTO items (ItemName) VALUES (?)", [newItemName])
    conn.commit()
    conn.close()
    return True

def addItems(itemId, storageId, quantityToAdd):
    if quantityToAdd is 0:
        return False

    quantityInStorage = __getNumOfItemsInStorage(itemId, storageId)

    if quantityInStorage is 0:
        __insertItemInStorage(itemId, storageId, quantityToAdd)
    else:
        __updateItemInStorage(itemId, storageId, quantityToAdd)
    return True

def removeItems(itemId, storageId, quantityToRemove):
    if quantityToRemove is 0:
        return False

    quantityInStorage = __getNumOfItemsInStorage(itemId, storageId)

    if quantityInStorage > quantityToRemove:
        __updateItemInStorage(itemId, storageId, quantityToRemove * -1)
    elif quantityInStorage == quantityToRemove:
        __removeItemFromStorage(itemId, storageId)
    else:
        return False

    return True

def moveItems(itemId, srcStorageId, dstStorageId, quantity):
    if quantity is 0:
        return False

    result = removeItems(itemId, srcStorageId, quantity);
    if result is False:
        return False

    result = addItems(itemId, dstStorageId, quantity)
    return result

def getItemIdByName(itemName):
    items = []

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT ItemId FROM items WHERE ItemName LIKE ?", (itemName,))

    while True:
        item = c.fetchone()
        if item is None:
            break
        items.append(item)
    conn.close()

    if len(items) == 1:
        return items[0][0], True
    return -1, False

def getItemNameById(itemId):

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT ItemName FROM items WHERE ItemId = ?", (itemId,))

    text = c.fetchone()
    conn.close()

    if  text is not None:
        return text[0], True
    return -1, False

def getStorageIdByName(storageName):
    storages = []

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT StorageId FROM storages WHERE StorageName LIKE ?", (storageName,))

    while True:
        storage = c.fetchone()
        if storage is None:
            break
        storages.append(storage)
    conn.close()

    if len(storages) == 1:
        return storages[0][0], True
    return -1, False

def getStorageNameById(storageId):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT StorageName FROM storages WHERE StorageId = ?", (storageId,))

    text = c.fetchone()
    conn.close()

    if  text is not None:
        return text[0], True
    return -1, False

#Получить список (ID детали и название детали) для всех деталей, в названии которых содержится строка itemName
def __searchItemsByName(itemName):
    items = []

    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute("SELECT ItemId, ItemName FROM items WHERE ItemName LIKE ?", ("%" + itemName + "%",))

    while True:
        item = c.fetchone()
        items.append(item)
        if item is None:
            break
    conn.close()
    return items

#Получить общее количество деталей во всех хранилищах
def __getNumOfItems(itemId):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('SELECT SUM(Quantity) FROM itemsAndStorages WHERE ItemId=?', [str(itemId)])
    text = c.fetchone()
    conn.close()

    try:
        numOfItems = int(text[0])
    except TypeError:
        numOfItems = 0

    return numOfItems

#Получить количество деталей в заданном хранилище
def __getNumOfItemsInStorage(itemId, storageId):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('SELECT Quantity FROM ItemsAndStorages WHERE StorageId=? AND ItemId=?', [str(storageId), str(itemId)])
    text = c.fetchone()
    conn.close()

    try:
        numOfItems = int(text[0])
    except TypeError:
        numOfItems = 0

    return numOfItems

#Добавить новую запись о детали в хранилище, где его еще нет
def __insertItemInStorage(itemId, storageId, quantity):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('INSERT INTO ItemsAndStorages (ItemId, StorageId, Quantity) VALUES (?, ?, ?)', [str(itemId), str(storageId), str(quantity)])
    conn.commit()
    conn.close()

#Изменить количество деталей в хранилище, где деталь уже присутствует
def __updateItemInStorage(itemId, storageId, quantityDiff):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('UPDATE ItemsAndStorages SET Quantity = Quantity+? WHERE ItemId=? AND StorageId=?', [str(quantityDiff), str(itemId), str(storageId)])
    conn.commit()
    conn.close()

#Удалить запись о детали в хранилище
def __removeItemFromStorage(itemId, storageId):
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('DELETE FROM ItemsAndStorages WHERE Itemid = ? AND StorageId = ?;', [str(itemId), str(storageId)])
    conn.commit()
    conn.close()


def main():
    print(getStorageNameById(33))

if __name__ == '__main__':
    main()