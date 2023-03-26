import random
import uno_ChkCon # Check Condition 
from queue import Queue

class game: # game 클래스 생성
    deckList = Queue() # 남은 덱
    openCard = [] # 공개된 카드
    playerList = [] # 플레이어 목록
    turnPlayer = 0 # 현재 턴 플레이어
    attackCard = 0 # 공격 카드 매수

    def __init__(self, player_list): # game 클래스 생성자
        self.playerList = player_list
        self.deckList = pile()
        self.openCard = pile()

    def __del__(self): # game class 소멸자
        pass

    def ready(self): #게임을 준비하는 메서드
        deckPreset = self.setDeck() # 사전에 정의한 덱 리스트
        
        self.deckList + deckPreset # 덱에 deckPreset을 넣는다.
        self.deckList.shuffle()


        for i in range(0, len(self.playerList)): # 각 플레이어들에게 카드를 나눠줍니다.
            self.playerList[i].draw(self.deckList, 5) # 나눠줄 카드의 개수 : 임의로 5로 설정했음
            print(self.playerList[i].playerName + ": ", self.playerList[i].allHand(),"\n")

        self.placeOpenCardZone(self.deckList.takeTopCard()) # 덱 맨 위에서 카드를 1장 오픈합니다.
        print("TopCard" +": " + self.openCard.cardList[-1].info()+"\n")

    def placeOpenCardZone(self, card): #OpenCardList에 카드를 놓습니다.
        self.openCard + [card]
        card.cardEffect()

    def setDeck(self): # 게임에 사용할 덱의 CardList를 반환합니다.
        tempList = []
        for i in range(0, 4): # 0~9까지의 4색 카드를 임시 리스트에 넣습니다.
            for j in range(0, 10):
                tempList.append(card(i, j))

        return tempList
    
    def executeTurn(self): # 하나의 턴을 실행합니다.
        
        if self.playerList[self.turnPlayer].isUser == True: # 턴 플레이어가 유저
                self.mainPhase()
                print("User",self.playerList[self.turnPlayer].playerName, "의 턴")
        else: # 턴 플레이어가 봇
            self.unoBot()
        
        result = self.endPhase()
        return result # 게임이 끝났는지, 승자는 누구인지
    
    def mainPhase(self):
        
        if self.attackCard > 0: # 공격 처리
            self.playerList[self.turnPlayer].draw(self.deckList, self.attackCard)
            self.attackCard = 0
        
        # 카드 내기 or 드로우 or 우노
    
    def endPhase(self):
        self.turnPlayer = (self.turnPlayer+1)%len(self.playerList)
        
        if (self.turnPlayer):
            return True
        
        return False
    
    def unoBot(self):
        print("bot",self.playerList[self.turnPlayer].playerName, "의 턴")

class pile: # pile 클래스 생성
    cardList = []

    def __init__(self, cardList = []): # player 클래스 생성자
        self.cardList = cardList

    def __del__(self): # player class 소멸자
        pass
    
    def shuffle(self): # pile의 카드를 섞습니다.
        random.shuffle(self.cardList)
        
    def takeTopCard(self): # 가장 위의 카드를 가져옵니다.
        result = self.cardList.pop()
        
        return result
    
    def __add__(self, op_2): # pile_2의 카드를 전부 옮깁니다.
        for i in op_2:
            self.cardList.append(i)
        op_2.clear() # 카드 옮겼으니 전부 지움
    
        
class player: # player 클래스 생성
    playerName = '' # 플레이어 이름
    isUser = True # user인가 bot인가 확인
    handCardList = [] # 들고 있는 카드

    def __init__(self, player_name, is_user): # player 클래스 생성자
        self.playerName = player_name
        self.isUser = is_user
        self.handCardList = []

    def __del__(self): # player class 소멸자
        pass

    def draw(self, pile, num): # game의 DeckList에서 카드를 뽑아 패로 가져옵니다.
        for i in range(0, num):
            self.handCardList.append(pile.takeTopCard())

    def allHand(self): # hand의 모든 카드에 대한 텍스트를 반환합니다.
        tempList = []
        handCardList = self.handCardList
        for i in range(0, len(handCardList)):
            tempList.append(handCardList[i].info())

        return tempList

    def delCard(self, index): # player의 카드를 삭제합니다. i : 삭제할 인덱스
        del self.handCardList[index]


    def delIndex(self, i, color): # 삭제할 카드의 인덱스를 찾습니다. i : 삭제할 숫자, color : 삭제할 색깔
        for c in self.handCardList:
            #c.cardNumber = 3
            #c.cardColor = green
            if c.number == i: # 이 부분이 수행 안됨
                #print(c.cardNumber)
                if c.color == color: # 이 부분이 수행 안됨
                    return player.handCardList.index(c) # c의 인덱스 값 리턴

    def printCurSta(self): # 현재 Player 카드 리스트
        print(self.playerName + ": ", self.allHand(), "\n")

class card: # 카드 클래스 생성
    '''
    cardColor, cardNumber 에서 card를 빼는게 어떨까요 ?
    '''
    color = -1 # 0: red, 1: green, 2: yellow, 3: blue, -1: none_color_card
    number = -1 # -1: special_card

    attack = -1 # 1 : +2 효과 기능, -1 : none
    changeSequence = -1 # 1 : 순서 변경 기능,-1 : none
    changeNumber = -1 # 1 : 숫자 변경 기능, -1 : none
    turnPass = -1 # 1 : 턴 넘기기 기능, -1 : none
    changeDeck = -1 # 1 : 덱 변경 기능, -1 : none
    changeColor = -1 # 1 : 컬러 변경 기능, -1 : none

    applyNumber = -1
    applyColor = -1


    def __init__(self, color, number, attack = -1, changeSequence = -1, changeNumber = -1, turnPass = -1, changeDeck = -1, changeColor = -1): # card 클래스 생성자

        # 특수 카드 생성시에는 인자로 기능들을 구분해야 하나 ?

        self.color = color
        self.number = number
        self.attack = attack
        self.changeSequence = changeSequence
        self.changeNumber = changeNumber
        self.turnPass = turnPass
        self.changeDeck = changeDeck
        self.changeColor = changeColor
        self.applyNumber = self.number # applyNumber 는 cardNumber 로 초기값 설정
        self.applyColor = self.color # applyColor 는 cardColor 로 초기값 설정




    def __del__(self): # card class 소멸자
        pass

    def cardEffect(self, game): # 특수 카드의 효과를 처리하기 위한 메서드.


        if self.attack == 1:
            game.attackCard += 2
        if self.changeSequence == 1:
            # game.playerList.reverse()
            tp = game.turnPlayer
            tmp_Lst = []

            for _ in range(len(game.playerList)):
                tp -= 1
                tmp_Lst.append(game.playerList[tp])

        if self.changeNumber == 1:
            applyNumber = int(input())

        if self.turnPass == 1:
            # turn pass turn flow 에서 넘겨야하나 ?
            game.jumpNumber += 1

        if self.changeDeck == 1:
            # change deck 가장 낮은 리스트 개수와 변경
            lstNum = []
            for p in game.playerList:
                lstNum.append(len(p.handCardList))

            MAX = lstNum.index(max(lstNum))
            MIN = lstNum.index(min(lstNum))

            game.playerList[MAX].handCardList, game.playerList[MIN].handCardList  = game.playerList[MIN].handCardList, game.playerList[MAX].handCardList

        if self.changeColor == 1:
            applyColor = int(input())


    def attack(self):
        player.draw()



    def info(self): # 카드 정보 표시
        colorDict = {-1:'None', 0:'red', 1:'green', 2:'yellow', 3:'blue'}
        return colorDict[self.color] + ' ' + str(self.number)

## 테스트용 ##
user1 = player('USER', True)
pc1 = player('PC1', False)
pc2 = player('PC2', False)
pc3 = player('PC3', False)

gamePlayerList = [user1, pc1, pc2, pc3]
g = game(gamePlayerList)
g.ready()

c = card(0, -1)
c1 = card(1, 1)
print(c1.color)
print(c1.number)
g.placeOpenCardZone(c)

g.executeTurn()
g.executeTurn()
g.executeTurn()
g.executeTurn()
g.executeTurn()
g.executeTurn()
g.executeTurn()