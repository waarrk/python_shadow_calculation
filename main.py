import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.colors import LightSource

# STLファイルの読み込み
your_mesh = mesh.Mesh.from_file('3DBenchy.stl', mode='rb')

# 図を作成
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# STLメッシュのプロット
poly3d = art3d.Poly3DCollection(your_mesh.vectors, alpha=1.0)
ax.add_collection3d(poly3d)

# スケーリング
scale = your_mesh.points.flatten()
ax.auto_scale_xyz(scale, scale, scale)

# ラベル付け
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 真上から光を当てる
light_direction = np.array([0, 0, 1])

# シェーディングの計算
face_colors = []

for i in range(len(your_mesh.vectors)):
    print(i, "/", len(your_mesh.vectors))
    p1, p2, p3 = your_mesh.vectors[i]
    norm = np.cross(p2 - p1, p3 - p1)
    norm_length = np.linalg.norm(norm)
    if norm_length > 0:
        norm = norm / norm_length

    intensity = np.dot(norm, light_direction)
    if intensity > 0:
        # 光が当たる部分は青
        color = (0, 0, 1)
    else:
        color = (1, 0, 0)  # 光が当たらない部分は赤

    face_colors.append(color)

    # 赤色の面の法線を描画
    if intensity <= 0:
        centroid = (p1 + p2 + p3) / 3
        # 法線ベクトルをスケーリング
        norm_length = 5
        ax.quiver(centroid[0], centroid[1], centroid[2],
                  norm[0] * norm_length, norm[1] * norm_length, norm[2] * norm_length, color='r')

# シェーディングの適用
poly3d.set_facecolor(face_colors)

# 表示
plt.show()


# STLファイルの体積を計算
volume, cog, inertia = mesh.get_mass_properties()
print("Volume: ", volume)

# 影の体積を計算
shadow_volume = 0
for i in range(len(mesh.vectors)):
    print(i, "/", len(mesh.vectors))
    p1, p2, p3 = mesh.vectors[i]
    norm = np.cross(p2 - p1, p3 - p1)
    norm_length = np.linalg.norm(norm)
    if norm_length > 0:
        norm = norm / norm_length

    intensity = np.dot(norm, light_direction)
    if intensity <= 0:
        shadow_volume += np.abs(np.dot(norm, cog - p1) / 6)

print("Shadow Volume: ", shadow_volume)
