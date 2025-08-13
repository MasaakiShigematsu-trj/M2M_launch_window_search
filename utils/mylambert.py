import numpy as np

def mylambert(GM, X1, X2, tof, string):
## 入力引数
## GM : 中心天体の重力定数
## X1, X2 : 出発天体と目標天体の６次元状態ベクトル [km, km/s]
## tof : 航行時間 [s]
## string : 'pro'ならば'prograde', 'retro'ならば'retrograde'

    R1 = X1[:3]  # X1（6次元）の最初の3つの要素を取り出す
    r1 = np.linalg.norm(R1)  # ノルムを計算する


    R2 = X2[:3]  # X2（6次元）の最初の3つの要素を取り出す
    r2 = np.linalg.norm(R2)  # ノルムを計算する


    cross12 = np.cross(R1, R2)  # R1とR2の外積を計算する
    theta = np.arccos(np.dot(R1, R2) / (r1*r2))  # 内積を計算し、アークコサインを取る


    if string == 'pro':
        if cross12[2] < 0:
            theta = 2 * np.pi - theta  # 第3象限または第4象限へ
    elif string == 'retro':
        if cross12[2] > 0:
            theta = 2 * np.pi - theta  # 第3象限または第4象限へ
   
    A = np.sin(theta) * np.sqrt(r1*r2/(1 - np.cos(theta)))
    
    ## 必要な関数の定義
    def C(z):
        if z == 0:
            return 1/2
        elif z > 0:
            return (1 - np.cos(np.sqrt(z))) / z
        elif z < 0:
            return (np.cosh(np.sqrt(-z)) - 1) / (-z)
    
    def S(z):
        if z == 0:
            return 1/6
        elif z > 0:
            return (np.sqrt(z) - np.sin(np.sqrt(z))) / z**(3/2)
        elif z < 0:
            return (np.sinh(np.sqrt(-z)) - np.sqrt(-z)) / (-z)**(3/2)

    def y(z):
        return r1 + r2 + A*(z*S(z) - 1)/np.sqrt(C(z))
    
    def F(z):
        return S(z)*(y(z)/C(z))**(3/2) + A*np.sqrt(y(z)) - np.sqrt(GM)*tof
    
    def dF(z):
        if z == 0:
            return np.sqrt(2)/40*y(0)**(3/2) + A/8*(np.sqrt(y(0)) + A*np.sqrt(1/(2*y(0))))
        else:
            return (y(z)/C(z))**(3/2) * ((C(z) - 3*S(z)/2/C(z))/2/z + 3*S(z)**2/4/C(z)) + A/8*(3*S(z)/C(z)*np.sqrt(y(z)) + A*np.sqrt(C(z)/y(z)))

    ## ニュートン法によるzの計算

    ## まずはy(z)が正の値になるまでzを増加させる
    z = 0  # 初期値
    while F(z) < 0:
       z = z + 0.1
       
    imax = 1000
    for i in range(imax):
        z = z - F(z)/dF(z)  # ニュートン法の更新式
        if y(z) < 0:
            print("y(z) is negative")
        elif abs(F(z)/dF(z)) < 1e-13:  # 収束条件
            break    

    ## ラグランジュの係数の計算
    f = 1 - y(z)/r1
    g = A*np.sqrt(y(z)/GM)
    gdot = 1 - y(z)/r2

    ## 速度ベクトルの計算
    V1 = (1/g)*(R2 - f*R1)
    V2 = (1/g)*(gdot*R2 - R1)

    Vp1 = X1[3:6]  # 出発天体のX1（6次元）の4-6番目の要素を取り出す
    Vp2 = X2[3:6]  # 到着天体のX2（6次元）の4-6番目の要素を取り出す

    Vinf1 = V1 - Vp1  # 出発無限遠速度(ベクトル)を計算する
    Vinf2 = V2 - Vp2  # 到着無限遠速度(ベクトル)を計算する
    Vinf1_norm = np.linalg.norm(Vinf1)  # Vinf1のノルムを計算する  
    Vinf2_norm = np.linalg.norm(Vinf2)  # Vinf2のノルムを計算する
    C3 = Vinf1_norm**2

    return Vinf1, Vinf2, Vinf1_norm, C3, Vinf2_norm, R1, V1, R2, V2  # 出発無限遠速度(ベクトル),到着無限遠速度(ベクトル)，C3を返す