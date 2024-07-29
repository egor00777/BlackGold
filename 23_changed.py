import math
import numpy as np 
import pandas as pd
import cv2
import random

class Neft():
    def __init__(self,photo):
        self.DATA=self.matrix(photo)
    def cur_price(self,h):
        p = 0.85
        k = 12.0 #эффективная проницаемость, мД (милиДарси)

        SRPLast = 270.0 #среднее пластовое давление, атм (атмосфер)
        zaboinoe_dav = 100.0 #забойное давление давление внизу скважины , атм
        vazkost = 1.4 #вязкость нефти, сП (сантиПуаз)
        obim_Koof = 1.15 #объёмный коэффициент нефти, д. ед.
        Rk = 800.0 #радиус контура объёма, из которого добывает скважина нефть, м ????????????
        Rc = 0.1 #радиус скважины, м
        SkinFack = 0.0 #скин − фактор (показывает ухудшение фильтрационных свойств пласта вблизи скважины)

        q = (p*k*h*(SRPLast - zaboinoe_dav))/(18.41*vazkost*obim_Koof*(math.log(Rk/Rc)-0.5+SkinFack))


        def qt(koofB,koofD):
            massiv = []

            for shagVR in range(480):
                QT = q/(1 + koofB * koofD * shagVR)**(1/koofB)
                massiv.append(QT*30)
            return massiv


        massiv=qt(1.4,0.12)
        price=[]
        price_tonna=53_135.006
        for n in range(40):
            try:
                summa=sum([massiv[i] for i in range(n*12,n*12+12)])
                cost=summa*price_tonna

                k=1/((1+0.17)**n)
                price.append(k*cost)
            except:
                break

        last_answer=sum(price)-60_000_000*9
        return last_answer
    
    def matrix(self,photo):
        img = cv2.imread(photo)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        df = pd.DataFrame([list(l) for l in hsv]).stack().apply(pd.Series)
        df.index.name = 'st'
        df.columns = list('RGB')

        df['color']= df.apply (self.f, axis=1)

        data=[[_ for _ in range(926)] for _ in range(664)]
        for i in range(len(data)):
            for j in range(len(data[0])):
                data[i][j]=df.loc[i,j]['color']

        data_sector_j=[]
        for i in range(664):
            for j in range(926//32):
                data_sector_j+=[sum(data[i][j*32:j*32+32])//32]

        data_sector_i=[]
        for x in range(0,len(data_sector_j),28):
            data_sector_i+=[data_sector_j[x:x+28]]

        data_sector=[]
        co=0
        cash=np.array([0 for _ in range(28)])
        for x in data_sector_i:
            x = np.array(x)
            if co==32: 
                co=0
                data_sector+=[list(cash)]
                cash=np.array([0 for _ in range(28)]) 
            cash+=x
            co+=1

        for i in range(len(data_sector)):
            for j in range(len(data_sector[0])):
                data_sector[i][j]//=32
        return data_sector
     
    def f(self,row):
        if row['R']>140: return 0
        elif row['R']>100 : return 10
        elif row['R']>80 : return 20

        elif row['R']>35 : return 30

        elif row['R']>20 : return 40
        else: return 50

    def answering(self,data_mine):

        data=self.DATA

        answer=0
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data_mine[i][j]:
                    answer+=self.cur_price(data[i][j])
        return answer

    def main(self):
        data=self.DATA
        data_mine=[[False for _ in range(len(data[0]))] for _ in range(len(data))]
        state = data_mine.copy()
        temp = 1.0
        n = 100
        i = 0
        while (i<n):
            temp *= 0.9
            i+=1
            new_state = state.copy()
            a = len(state)
            b = len(state[0])
            ra = random.randint(0,a-1)
            rb = random.randint(0,b-1)
            state[ra][rb] = not state[ra][rb]
            f_old =self.answering(state)
            f_new = self.answering(new_state)
            if f_old== f_new: continue
            if (f_old < f_new):
                state = new_state.copy() 
                continue
            if (random.uniform(0,1)< math.exp(-(f_old - f_new)/temp)):
                state = new_state.copy() 
                continue
            
        return self.answering(state),state

    

neft=Neft('new_test_photo.png')
print(neft.main())