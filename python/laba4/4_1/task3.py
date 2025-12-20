import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path


#Somebody once told me the world is gonna roll me
#I ain't the sharpest tool in the shed

def draw_shrek(ax):
    head = patches.Ellipse((0, 2.8), width=5.0, height=5.8,
                           facecolor='#9acd32', edgecolor='black', linewidth=2.5)
    ax.add_patch(head)

    left_ear = patches.FancyBboxPatch((-3.1, 3.6), 1.1, 0.8, boxstyle="round,pad=0.2",
                                      facecolor='#9acd32', edgecolor='black', linewidth=2)
    right_ear = patches.FancyBboxPatch((2.0, 3.6), 1.1, 0.8, boxstyle="round,pad=0.2",
                                       facecolor='#9acd32', edgecolor='black', linewidth=2)
    ax.add_patch(left_ear)
    ax.add_patch(right_ear)

    for x in [-1.0, 1.0]:
        ax.add_patch(patches.Circle((x, 2.9), 0.55, facecolor='white', edgecolor='black', linewidth=1.5))
        ax.add_patch(patches.Circle((x, 2.8), 0.25, facecolor='saddlebrown', edgecolor='black', linewidth=1))
        ax.add_patch(patches.Circle((x - 0.05, 2.85), 0.08, facecolor='white', edgecolor='none'))  # блик

    ax.plot([-1.6, -0.4], [3.7, 3.5], color='black', linewidth=2.5)
    ax.plot([0.4, 1.6], [3.5, 3.7], color='black', linewidth=2.5)

    ax.add_patch(patches.Ellipse((0, 2.1), 1.1, 0.6,
                                 facecolor='#8dc63f', edgecolor='black', linewidth=2))
    ax.plot([-0.3, -0.15], [2.05, 1.95], color='black', linewidth=1.8)
    ax.plot([0.15, 0.3], [2.05, 1.95], color='black', linewidth=1.8)

    mouth_path = Path(
        [(-1.2, 1.4), (-0.6, 1.1), (0.6, 1.1), (1.2, 1.4)],
        [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    )
    mouth = patches.PathPatch(mouth_path, facecolor='none', edgecolor='black', linewidth=2.5)
    ax.add_patch(mouth)

    body = patches.Ellipse((0, -2.8), 7.0, 8.0,
                           facecolor='#f5deb3', edgecolor='black', linewidth=2.5)
    ax.add_patch(body)

    vest = patches.Ellipse((0, -2.8), 6.3, 7.0,
                           facecolor='#8b4513', edgecolor='black', linewidth=2.5)
    ax.add_patch(vest)

    ax.add_patch(patches.Circle((-3.3, -0.6), 1.0,
                                facecolor='#f5deb3', edgecolor='black', linewidth=2.5))
    ax.add_patch(patches.Circle((3.3, -0.6), 1.0,
                                facecolor='#f5deb3', edgecolor='black', linewidth=2.5))

fig, ax = plt.subplots(figsize=(7, 9))
ax.set_xlim(-6, 6)
ax.set_ylim(-7, 6)
ax.set_aspect('equal')
plt.axis('off')

draw_shrek(ax)

plt.tight_layout()
plt.show()
