from datetime import datetime
import os

def GetFilePath(fileName):
    """Определяет местоположение исполняемого файла и его родителя.
    Определяет используемый разделитель в строке пути.
    Возвращает строку - созданный путь для будущего файла справочника.
    """
    filePath = os.path.abspath(__file__)
    fileParent = (os.path.dirname(os.path.normpath(filePath)))
    sep = "/" if ("/" in filePath) else "\\"
    return fileParent + sep + fileName

def CreateFile(filePath):
    """Создание файла, если он еще не существует"""
    if (not os.path.exists(filePath)):
        with open(filePath, "w+", encoding="utf-8") as myFile:
            myFile.write("")

def GetMyList(filePath):
    """Вернуть блокнот в виде листа заметок"""
    with open(filePath, "r", encoding="utf-8") as myFile:
        myList = myFile.readlines()
    return myList

def ShowNotes(filePath):
    """Пункт меню. Показать весь блокнот заметок"""
    myList = GetMyList(filePath)
    report = "Показ блокнота заметок:\n"
    for myRow in myList:
        report += myRow.replace(";", " ")
    tmp = report
    return report, tmp

def AddNote(filePath):
    """Пункт меню. Добавить заметку"""
    print("Ввод новых данных.")
    noteHeader = input("Введите заголовок заметки: ")
    noteBody = input("Введите тело заметки: ")
    noteDate = datetime.now()
    noteId = f"ID{noteDate.year}{noteDate.month}{noteDate.day}{noteDate.hour}{noteDate.minute}{noteDate.second}{noteDate.microsecond}"
    newNoteRow = f"{noteHeader};{noteBody};{noteId};{noteDate};\n"
    mySet = set(GetMyList(filePath))
    if newNoteRow in mySet:
        report = f"Заметка '{noteHeader}. {noteBody}. {noteId} от {noteDate}' уже существует."
        tmp = "Error"
        return report, tmp
    with open(filePath, "a+", encoding="utf-8") as myFile:
        myFile.write(newNoteRow)
    report = f"Заметка '{noteHeader}. {noteBody}. {noteId} от {noteDate}' добавлена."
    tmp = (noteHeader, noteBody, noteId, noteDate)
    return report, tmp

def FindNote(filePath):
    """Пункт меню. Найти заметку"""
    findText = input("Введите текст для поиска заметки: ")
    myList = GetMyList(filePath)
    report = f"Текст '{findText}' не найден."
    tmp = "Error"
    for rowNumber in range(0, len(myList)):
        if findText in myList[rowNumber]:
            note = myList[rowNumber].replace(";", " ").replace("\n", "")
            report = f"На строке № {rowNumber} найдена заметка: {note}"
            tmp = rowNumber
            return report, tmp
    return report, tmp

def DeleteNote(filePath):
    """Пункт меню. Удалить заметку"""
    myList = GetMyList(filePath)
    FindNoteReport, FindNoteTMP = FindNote(filePath)
    if (FindNoteTMP == "Error"):         # если не удалось найти
        report = FindNoteReport
        tmp = "Error"
        return report, tmp
    rowForDel = FindNoteTMP                                             # фикс номера строки
    note = myList[FindNoteTMP].replace(";", " ").replace("\n", "")      # для отчета в консоль
    myList.remove(myList[FindNoteTMP])                                  # удалить
    with open(filePath, "w+", encoding="utf-8") as myFile:              # перезаписать в файл изменения
        myFile.write("".join(myList))
    report = f"Заметка '{note}' удалена."
    tmp = rowForDel
    return report, tmp

def EditNote(filePath):
    """Пункт меню. Редактировать заметку"""
    # 1. удалить
    DeleteNoteReport, DeleteNoteTMP = DeleteNote(filePath)
    if (DeleteNoteTMP == "Error"):         # если не удалось удалить (т.е скорее всего найти)
        report = DeleteNoteReport
        tmp = "Error"
        return report, tmp
    # 2. разбить список на два
    myList = GetMyList(filePath)
    myList1 = myList[:DeleteNoteTMP]
    myList2 = myList[DeleteNoteTMP:]
    # 3. записать первый список в файл
    with open(filePath, "w+", encoding="utf-8") as myFile:
        myFile.write("".join(myList1))
    # 4. вызов функции добавления нового контакта
    AddNoteReport, AddNoteTMP = AddNote(filePath)
    if (AddNoteTMP == "Error"):     # если не удалось добавить (т.е скорее всего такой контакт уже есть)
        report = AddNoteReport
        tmp = "Error"
        return report, tmp
    # 5. дописать в конец второй список
    with open(filePath, "a+", encoding="utf-8") as myFile:
        myFile.write("".join(myList2))
    # 6. отчитаться
    report = f"Заметка '{AddNoteTMP[0]}. {AddNoteTMP[1]}. {AddNoteTMP[2]} от {AddNoteTMP[3]}' в строке {DeleteNoteTMP} отредактирована."
    tmp = DeleteNoteTMP
    return report, tmp

def ExportNotes(filePath):
    """Пункт меню. Экспортировать заметки"""
    myList = GetMyList(filePath)                            # данные для экспорта в файл
    dateName = "Notebook_" + str(datetime.now()).replace(" ", "").replace("-", "").replace(".", "").replace(":", "") + ".csv"
    fileParent = (os.path.dirname(os.path.normpath(filePath)))
    sep = "/" if ("/" in filePath) else "\\"
    exportFilePath = fileParent + sep + dateName                    # имя экспортного файла
    CreateFile(exportFilePath)                                      # создание файла - на всякий - необязательно
    with open(exportFilePath, "a+", encoding="utf-8") as myFile:    # запись данных в файл
        myFile.write("".join(myList))
    report = f"Выполнен экспорт в файл: {exportFilePath}"
    tmp = exportFilePath
    return report, tmp

def ImportNotes(filePath):
    """Пункт меню. Импортировать заметки"""
    fileParent = (os.path.dirname(os.path.normpath(filePath)))
    sep = "/" if ("/" in filePath) else "\\"
    defaultPathForImport = fileParent + sep + "FileForImport.csv"
    importFilePath = input(f"Введите путь к файлу csv для импортирования данных с файла.\n(Enter -  ввод адреса по умолчанию: '{defaultPathForImport}') ")
    if importFilePath == "": importFilePath = defaultPathForImport
    if (not os.path.exists(importFilePath)):
        report = f"Неверный адрес файла: {importFilePath}"
        tmp = "Error"
        return report, tmp
    listFromImport = GetMyList(importFilePath)
    with open(filePath, "a+", encoding="utf-8") as myFile:
        myFile.write("".join(listFromImport))
    report = f"Данные из файла '{importFilePath}' импортированы."
    tmp = importFilePath
    return report, tmp

def ExitProgram(filePath):
    """Пункт меню. Завершить программу через стандартный механизм выброса исключения"""
    raise SystemExit

def GetMenuDictionary():
    """Создать словарь для пунктов меню.
    Ключ - порядковый номер.
    Значение - кортеж из ссылки на функцию и текстового описания.
    """
    menuDict = {
        1: (ShowNotes, "Показать блокнот"),
        2: (AddNote, "Добавить заметку"),
        3: (FindNote, "Найти заметку"),
        4: (DeleteNote, "Удалить заметку"),
        5: (EditNote, "Редактировать заметку"),
        6: (ExportNotes, "Экспортировать заметки"),
        7: (ImportNotes, "Импортировать заметки"),
        8: (ExitProgram,    "Выйти из программы")
    }
    return menuDict

def GetActionFromMenu(menuDict, filePath):
    """Показ меню и выбор действия"""
    print("Меню:")
    for key in menuDict:
        print(f"{key}. {menuDict[key][1]}.")
    actionFromMenu = int(input("Выберите действие: "))
    return actionFromMenu

def main() -> None:
    """Точка входа"""
    fileName = "Notebook.csv"                   # имя файла блокнота
    filePath = GetFilePath(fileName)            # формирование пути для блокнота (рядом с Note.py)
    CreateFile(filePath)                        # на всякий случай во избежание проблем - необязательно
    menuDict = GetMenuDictionary()              # создание меню
    report = ""                                 # отчет о проделанной работе по выбранному действию
    while (True):                               # бесконечный цикл выбора пункта меню (завершается спец.пунктом)
        actionFromMenu = GetActionFromMenu(menuDict, filePath)
        # Каждый метод возвращает report и tmp
        # report - отчет для вывода на консоль - для пользователя
        # tmp - какой-то объект для технических целей - в зависимости от метода - для программиста
        report, tmp = menuDict[actionFromMenu][0](filePath)
        os.system('cls||clear')
        print(report)

if __name__ == '__main__':
    main()
