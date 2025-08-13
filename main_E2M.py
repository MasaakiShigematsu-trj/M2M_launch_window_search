import numpy as np
from astropy.time import Time
from utils.mylambert import mylambert


GM_sun = 1.32712440041279419e11 # 太陽の重力定数 [km^3/s^2]

# 地球のエフェメリス情報を読み込み
ephemeris_E = []

# with open("data_E2M/f1_earth.txt", "r") as file:
# with open("data_E2M/f2_earth.txt", "r") as file:
with open("data_E2M/f3_earth.txt", "r") as file:
    buffer = []  # 一時的に行を保持するリスト
    for line in file:
        # 行をバッファに追加
        buffer.append(line.strip())

        # バッファに4行たまったら処理を開始
        if len(buffer) == 4:
            for i, buf_line in enumerate(buffer):
                if "= A.D." in buf_line:  # `= A.D.`を含む場合
                    # `=A.D.` の前の値を取得
                    JD_value = buf_line.split()[0]
                    
                    # 次の行の3つの値を取得
                    r_line = buffer[i + 1].split() if i + 1 < len(buffer) else []
                    v_line = buffer[i + 2].split() if i + 2 < len(buffer) else []
                    rg_line = buffer[i + 3].split() if i + 3 < len(buffer) else []
                    
                    if len(r_line) >= 3 and len(v_line) >= 3:
                        values = [float(JD_value)] + list(map(float, r_line[:3])) + list(map(float, v_line[:3])) + [float(rg_line[1])]
                        ephemeris_E.append(values)
            
            # 処理後、バッファをクリア
            buffer = []

# 火星のエフェメリス情報を読み込み
ephemeris_M = []

# with open("data_E2M/f1_mars.txt", "r") as file:
# with open("data_E2M/f2_mars.txt", "r") as file:
with open("data_E2M/f3_mars.txt", "r") as file:
    buffer = []  # 一時的に行を保持するリスト
    for line in file:
        # 行をバッファに追加
        buffer.append(line.strip())

        # バッファに4行たまったら処理を開始
        if len(buffer) == 4:
            for i, buf_line in enumerate(buffer):
                if "= A.D." in buf_line:  # `= A.D.`を含む場合
                    # `=A.D.` の前の値を取得
                    JD_value = buf_line.split()[0]
                    
                    # 次の行の3つの値を取得
                    r_line = buffer[i + 1].split() if i + 1 < len(buffer) else []
                    v_line = buffer[i + 2].split() if i + 2 < len(buffer) else []
                    rg_line = buffer[i + 3].split() if i + 3 < len(buffer) else []
                    
                    if len(r_line) >= 3 and len(v_line) >= 3:
                        values = [float(JD_value)] + list(map(float, r_line[:3])) + list(map(float, v_line[:3])) + [float(rg_line[1])]
                        ephemeris_M.append(values)
                        
            
            # 処理後、バッファをクリア
            buffer = []

print(len(ephemeris_E), len(ephemeris_M))

result = []
result_all = []
result_selected = []
for i_dep in range(len(ephemeris_E)):
  print(len(ephemeris_E) - i_dep) # 進捗表示
  for i_arr in range(len(ephemeris_M)):
    tof = (ephemeris_M[i_arr][0] - ephemeris_E[i_dep][0])*24*60*60  # [s]
    if tof > 50*24*60*60:
      try:
        X1 = np.array(ephemeris_E[i_dep][1:7])  # 地球の初期状態ベクトル
        X2 = np.array(ephemeris_M[i_arr][1:7])  # 火星の初期状態ベクトル
        RG1 = ephemeris_E[i_dep][7]  # 太陽-地球間の距離
        RG2 = ephemeris_M[i_arr][7]  # 太陽-火星間の距離
        string = 'pro'
        l = mylambert(GM_sun, X1, X2, tof, string)
        dep_date = Time(ephemeris_E[i_dep][0], format='jd').to_datetime()
        arr_date = Time(ephemeris_M[i_arr][0], format='jd').to_datetime()
      except ValueError:
        continue
      else:
        tof_days = tof / (24*60*60)
        if l[2] < 10: 
          result.append([ephemeris_E[i_dep][0], ephemeris_M[i_arr][0], tof_days, l[2], l[3], l[4]])  # ポークチョップ図を描くために必要最低限な情報
          result_all.append([dep_date, ephemeris_E[i_dep][0], arr_date, ephemeris_M[i_arr][0], l[2], l[4], l[1], X2])  # 位置ベクトルと速度ベクトルを含む詳細な情報
          result_selected.append([ephemeris_E[i_dep][0], ephemeris_M[i_arr][0], l[2], l[4], l[1][0], l[1][1], l[1][2], X2[0], X2[1], X2[2], X2[3], X2[4], X2[5]])  # 位置ベクトルと速度ベクトルを含む詳細な情報(数値のみ)
        else:
          result.append([ephemeris_E[i_dep][0], ephemeris_M[i_arr][0], tof_days, float('nan'), float('nan'), float('nan')])
          result_all.append([dep_date, ephemeris_E[i_dep][0], arr_date, ephemeris_M[i_arr][0], float('nan'), float('nan'), float('nan'), float('nan')])  # 詳細な情報はNaNで埋める
          result_selected.append([ephemeris_E[i_dep][0], ephemeris_M[i_arr][0], float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')])  # 位置ベクトルと速度ベクトルを含む詳細な情報(数値のみ)
        
# with open("result_E2M/E2M_f1_plot.txt", "w") as file:
# with open("result_E2M/E2M_f2_plot.txt", "w") as file:
with open("result_E2M/E2M_f3_plot.txt", "w") as file:
  for res in result:
    file.write(" ".join(map(str, res)) + "\n")

# with open("result_E2M/E2M_f1_all.txt", "w") as file:
# with open("result_E2M/E2M_f2_all.txt", "w") as file:
with open("result_E2M/E2M_f3_all.txt", "w") as file:
    for res_all in result_all:
        formatted = []
        for item in res_all:
            if isinstance(item, np.ndarray):  # ベクトルは1行の文字列に
                formatted.append("[" + " ".join(f"{x:.8e}" for x in item) + "]")
            elif isinstance(item, float):
                formatted.append(f"{item:.8f}")  # 小数は8桁で揃える
            else:
                formatted.append(str(item))  # 日付やJDなどはそのまま
        file.write(" ".join(formatted) + "\n")

# with open("result_E2M/E2M_f1_selected.txt", "w") as file:
# with open("result_E2M/E2M_f2_selected.txt", "w") as file:
with open("result_E2M/E2M_f3_selected.txt", "w") as file:
  for res_sel in result_selected:
    file.write(" ".join(map(str, res_sel)) + "\n")