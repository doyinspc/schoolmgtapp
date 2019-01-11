import random
from connect import Db


def words():
    x = ['a', 'b', 'c', 'd','e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd','e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    y = random.randint(3, 15)
    newword = random.sample(x, y)
    nw = ''.join(map(str, newword))
    return nw

def addrs():
    x = ['a', 'b', 'c', 'd','e', 'f', 'g', ' ', ' ', ' ', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd','e', 'f', 'g', ' ', ' ', ' ', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd','e', 'f', 'g', ' ', ' ', ' ', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd','e', 'f', 'g', ' ', ' ', ' ', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd','e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 1, 2, 3, 4, 5, 6, 7, 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    y = random.randint(20, 100)
    newword = random.sample(x, y)
    nw = ''.join(map(str, newword))
    return nw

def phons():
    x = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,0,0,0]
    z = ['0801', '0802', '0803', '0804', '0805', '0806', '0807', '0807', '0809', '0701', '0901', '0813' ]
    newword = random.sample(x, 7)
    nw = ''.join(map(str, newword))
    nw1 = random.choice(z)+str(nw)
    return nw1

def rdate():
    return str(random.randint(1, 30))+'/'+str(random.randint(1, 12))+'/'+str(random.randint(1998, 2010))
   
def rdates():
    return str(random.randint(1, 30))+'/'+str(random.randint(1, 12))+'/'+str(random.randint(2012, 2018))


relations = ['Father', 'Mother', 'Aunt', 'Uncle', 'Grand Parent', 'Guardian', 'Others']
g = Db()
g.createTable(1)

for i in range(1, 2000):
        print(rdate())
        arr = {}
        arr['schno'] = i + 3000
        arr['surname'] = words()
        arr['firstname'] = words()
        arr['othername'] = words()
        arr['soo'] = random.choice(['kaduna', 'osun','enugu', 'ekiti', 'kano', 'lagos', 'plateau', 'benue'])
        arr['lga'] = random.choice(['chikun', 'ife','ileku', 'ikeja', 'ilesha', 'jos'])
        arr['nation'] = 'nigeria'
        arr['gender'] = random.choice([0, 1])
        arr['addr'] = addrs()
        arr['dob'] = rdate()
        arr['admit'] = rdates()
        arr['g1'] = arr['surname']+' '+words()+' '+words()
        arr['g1rel'] = random.choice(relations)
        arr['g1p1'] = phons()
        arr['g1p2'] = phons()
        arr['g1email'] = arr['surname']+'@'+random.choice(['yahoo', 'gmail'])+'.com'
        arr['g1addr'] = addrs()
        arr['g2'] = arr['firstname']+' '+words()+' '+words()
        arr['g2rel'] = random.choice(relations)
        arr['g2p1'] = phons()
        arr['g2p2'] = phons()
        arr['g2email'] = words()+'@'+random.choice(['yahoo', 'gmail', 'hotmail'])+'.com'
        arr['g2addr'] = addrs()
        arr['active'] = random.choice([0,0,0,0,0,0,0,1])
        
        
        
        if((arr['surname'] > 0) and (arr['firstname'] > 0) and (arr['surname'] > 0)):
            g.insert('students', arr)    
    
   # print(surname)
    