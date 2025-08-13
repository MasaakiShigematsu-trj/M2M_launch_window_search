import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
import matplotlib.dates as mdates

# ファイルから結果を読み込み
# data = np.loadtxt("result_M2E/M2E_f1_plot.txt")
data = np.loadtxt("result_M2E/M2E_f2_plot.txt")
# data = np.loadtxt("result_M2E/M2E_f3_plot.txt")

# データを各軸に分解
dep_JD = data[:, 0]
arr_JD = data[:, 1]
tof_days = data[:, 2]
vinf1 = data[:, 3]
C3 = data[:, 4]
vinf2 = data[:, 5]

# 出発日と到着日を一意の値に
dep_unique = np.unique(dep_JD)
arr_unique = np.unique(arr_JD)

# メッシュグリッドを作成
Dep_JD_grid, Arr_JD_grid = np.meshgrid(dep_unique, arr_unique)

# グリッドを初期化
vinf1_grid = np.full_like(Dep_JD_grid, np.nan, dtype=np.float64)
vinf2_grid = np.full_like(Dep_JD_grid, np.nan, dtype=np.float64)
C3_grid = np.full_like(Dep_JD_grid, np.nan, dtype=np.float64)
TOF_grid = np.full_like(Dep_JD_grid, np.nan, dtype=np.float64)

# 各データを対応するグリッドに格納
for i in range(len(data)):
    dep_idx = np.where(dep_unique == dep_JD[i])[0][0]
    arr_idx = np.where(arr_unique == arr_JD[i])[0][0]
    vinf1_grid[arr_idx, dep_idx] = vinf1[i]
    C3_grid[arr_idx, dep_idx] = C3[i]
    vinf2_grid[arr_idx, dep_idx] = vinf2[i]
    TOF_grid[arr_idx, dep_idx] = tof_days[i]

# JDをdatetimeに変換
dep_dates = Time(dep_unique, format='jd').to_datetime()
arr_dates = Time(arr_unique, format='jd').to_datetime()

Dep_grid_dates, Arr_grid_dates = np.meshgrid(dep_dates, arr_dates)

# 等高線のレベルを指定
levels_vinf1 = [2, 3, 4, 5, 6, 7, 8, 9, 10]
levels_vinf2 = [2, 3, 4, 5, 6, 7, 8, 9, 10]
levels_C3 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
levels_TOF = [100, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100]

# 等高線の描画関数
def plot_contours(grid, levels, title, filename, colorbar_label, cmap='jet'):
    plt.figure(figsize=(10, 8))

    # 塗りつぶし等高線
    cp = plt.contourf(Dep_grid_dates, Arr_grid_dates, grid, levels=levels, cmap=cmap, extend='both')

    # 等高線（線だけ）
    cs = plt.contour(Dep_grid_dates, Arr_grid_dates, grid, levels=levels, colors='black', linewidths=0.8)
    TOFs = plt.contour(Dep_grid_dates, Arr_grid_dates, TOF_grid, levels=levels_TOF, colors='black', linewidths=0.5)

    # ラベルつける
    plt.clabel(cs, inline=True, fontsize=8, fmt="%.0f")
    plt.clabel(TOFs, inline=True, fontsize=8, fmt="%.0f")

    # カラーバー
    plt.colorbar(cp, label=colorbar_label)

    # 軸ラベルとか
    plt.xlabel("Departure Date")
    plt.ylabel("Arrival Date")
    plt.title(title)

    # 日付フォーマットにする
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # x軸・y軸の日付の間隔を月単位で調整
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().yaxis.set_major_locator(mdates.MonthLocator(interval=1))

    # x軸とy軸の範囲を調整（見たい範囲を指定）
    plt.xlim([min(dep_dates), max(dep_dates)])  # 出発日の範囲
    plt.ylim([min(arr_dates), max(arr_dates)])  # 到着日の範囲

    # x軸の目盛りを斜めに回転
    plt.xticks(rotation=90)

    plt.grid(True)

    # 保存
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    # 表示
    # plt.show(block=True)
    plt.show()

# 各等高線を描画して保存
# plot_contours(vinf1_grid, levels_vinf1, "Earth to Mars : Vinf1", "plots_M2E/Vinf1_M2E_f1.png", "Vinf1 [km/s]")
# plot_contours(C3_grid, levels_C3, "Earth to Mars : C3",          "plots_M2E/C3_M2E_f1.png",    "C3 [km^2/s^2]")
# plot_contours(vinf2_grid, levels_vinf2, "Earth to Mars : Vinf2", "plots_M2E/Vinf2_M2E_f1.png", "Vinf2 [km/s]")

plot_contours(vinf1_grid, levels_vinf1, "Earth to Mars : Vinf1", "plots_M2E/Vinf1_M2E_f2.png", "Vinf1 [km/s]")
plot_contours(C3_grid, levels_C3, "Earth to Mars : C3",          "plots_M2E/C3_M2E_f2.png",    "C3 [km^2/s^2]")
plot_contours(vinf2_grid, levels_vinf2, "Earth to Mars : Vinf2", "plots_M2E/Vinf2_M2E_f2.png", "Vinf2 [km/s]")

# plot_contours(vinf1_grid, levels_vinf1, "Earth to Mars : Vinf1", "plots_M2E/Vinf1_M2E_f3.png", "Vinf1 [km/s]")
# plot_contours(C3_grid, levels_C3, "Earth to Mars : C3",          "plots_M2E/C3_M2E_f3.png",    "C3 [km^2/s^2]")
# plot_contours(vinf2_grid, levels_vinf2, "Earth to Mars : Vinf2", "plots_M2E/Vinf2_M2E_f3.png", "Vinf2 [km/s]")