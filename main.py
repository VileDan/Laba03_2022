from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import json

# Загрузка форм
AutorizationForm, AutorizationWindow = uic.loadUiType("cipherUi_Autorization.ui")
app = QApplication([])
autorizationWindow = AutorizationWindow()
autorizationForm = AutorizationForm()
autorizationForm.setupUi(autorizationWindow)
CipherForm, CipherWindow = uic.loadUiType("cipherUi_Cipher.ui")
cipherWindow = CipherWindow()
cipherForm = CipherForm()
cipherForm.setupUi(cipherWindow)

autorizationWindow.show()
# cipherWindow.show()

# Загрузка списка пользователей
usersList = {}
try:
    with open('users/userList.json') as json_file:
        usersList = json.load(json_file)
except Exception:
    with open('users/userList.json', 'w') as outfile:
        usersList = {"users": []}
        json.dump(usersList, outfile)

cipherKey = 123654
cipherWord = "vladosdev"
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
cipherAlphabet = ['A', 'D', 'F', 'G', 'V', 'X']

# Авторизация
inputLogin = ""
inputPassword = ""


def formOpen():
    cipherWindow.show()
    autorizationWindow.close()


def signUp():
    if len(autorizationForm.loginBox.text()) > 0 and len(autorizationForm.passwordBox.text()) > 0:
        inputLogin = autorizationForm.loginBox.text()
        inputPassword = autorizationForm.passwordBox.text()
        userCreate(inputLogin, inputPassword)


def signIn():
    if len(autorizationForm.loginBox.text()) > 0 and len(autorizationForm.passwordBox.text()) > 0:
        inputLogin = autorizationForm.loginBox.text()
        inputPassword = autorizationForm.passwordBox.text()
        isUserExist = False
        neededPassword = ""
        for x in range(len(usersList["users"])):
            if (usersList["users"][x]["login"] == inputLogin):
                isUserExist = True
                neededPassword = usersList["users"][x]["password"]
                break
        if not isUserExist or inputPassword != neededPassword:
            autorizationForm.status_label.setText("Неправильный пользователь или пароль")
        elif isUserExist and inputPassword == neededPassword:
            autorizationForm.status_label.setText("Успешный вход")
            formOpen()
            cipherForm.hello_label.setText("Здравствуйте, {0}! Что будете шифровать сегодня?".format(inputLogin))
    else:
        autorizationForm.status_label.setText("Пустые поля")


def userCreate(iL, iP):
    isUserExist = False
    # Проверка, есть ли пользователь
    if len(usersList["users"]) > 0:
        for x in range(len(usersList["users"])):
            if usersList["users"][x]["login"] == iL:
                autorizationForm.status_label.setText(
                    "Такой пользователь уже существует! Пароль восстановить невозможно(")
                print("Такой пользователь уже существует! Пароль восстановить невозможно(")
                isUserExist = True
                break
    else:
        autorizationForm.status_label.setText("Пустые поля")
    if not isUserExist:
        usersList["users"].append({"login": iL, "password": iP})
        with open('users/userList.json', 'w') as outfile:
            json.dump(usersList, outfile)
            autorizationForm.status_label.setText("Регистрация успешна")
            print("Регистрация успешна!")
            formOpen()
            cipherForm.hello_label.setText("Здравствуйте, {0}! Что будете шифровать сегодня?".format(iL))


autorizationForm.signUpButton.clicked.connect(signUp)
autorizationForm.signInButton.clicked.connect(signIn)


# Сам шифратор


def normalTextInput():
    print("Проверка возможности...")
    message = cipherForm.normalTextBox.toPlainText()
    # Удаляем пробелы
    workText = message.replace(' ', '')
    if isRightMessage(workText) or len(cipherForm.cipherKeyBox.text()) == 0:
        cipherMessage(workText)
        print("Первый этап шифрования завершен")
    else:
        print("Нарушены правила шифрования")


def cipherMessage(txt):
    cipherWord = cipherForm.cipherWordBox.text()
    cipherKey = cipherForm.cipherKeyBox.text()
    polibiusSquare = [[]]
    firstStepCipher = ""
    finalStepCipher = ""
    coloumn = [[]]
    print("Начинается шифрование")
    polibiusSquare = polibiusSquareForm(cipherWord)
    for letter in txt:
        indices = [(i, x.index(letter)) for i, x in enumerate(polibiusSquare) if letter in x]
        firstStepCipher += cipherAlphabet[indices[0][0]] + cipherAlphabet[indices[0][1]]
    print("\n")
    coloumn = coloumnForm(firstStepCipher)
    finalStepCipher = coloumnShuffle(coloumn, cipherKey)
    cipherForm.cipherTextBox.setPlainText(finalStepCipher)
    #Запись в файл
    outputFile = "{0}\nКлюч колонок: {1}\nКлючевое слово: {2}".format(finalStepCipher, cipherKey, cipherWord)
    with open("cipherMessage.txt", "w") as file:
        file.write(outputFile)


def coloumnShuffle(clm, key):
    order = key.split(' ')
    print(clm[0][int(order[0])])
    itog = ""
    for y in range(6):
        for x in range(6):
            try:
                itog += clm[x][int(order[y])]
            except Exception:
                itog += ""
    return itog


def coloumnForm(cipher):
    coloumns = [[]]
    counter = 0
    for x in range(6):
        coloumns.append([])
        for y in range(6):
            if counter < len(cipher):
                coloumns[x].append(cipher[counter])
                counter += 1
        print(coloumns[x])
    return coloumns


def polibiusSquareForm(word):
    polibiusSquare = [[]]
    isWordIsOver = False
    counterOfWordLetters = 0
    counterWithoutRepeat = 0
    letterWhatWas = []  # Буквы которые уже встречались
    for x in range(6):
        polibiusSquare.append([])
        for y in range(6):
            # Разбираем сначала слово по буквам и если буква уже была не добавляем
            for I in range(len(word)):
                if word[I] not in letterWhatWas:
                    # print(cipherWord[counterForWord])
                    polibiusSquare[x].append(word[I])
                    letterWhatWas.append(word[I])
                    counterOfWordLetters += 1
                    break
            else:
                isWordIsOver = True
            if isWordIsOver:
                for J in range(len(alphabet)):
                    if alphabet[J] not in letterWhatWas:
                        # print(cipherWord[counterForWord])
                        polibiusSquare[x].append(alphabet[J])
                        letterWhatWas.append(alphabet[J])
                        break
        print(polibiusSquare[x])

    return polibiusSquare


def isRightMessage(txt):
    # Ищем с сообщении все соблюдения правил шифрования т.е. все ли буквы латинского алфавита или цифры и нет символов
    for x in txt:
        isEquals = False
        for y in range(len(alphabet)):
            if x == alphabet[y]:
                isEquals = True
                break
        if not isEquals:
            return False
    return True


cipherForm.cipherButton.clicked.connect(normalTextInput)

app.exec_()
