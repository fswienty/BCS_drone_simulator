import sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12})

labels = [2, 4, 6, 8]
opt_means = [5.4, 6, 6.8, 12.5]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

data = [[5.300239324569702, 5.4547998905181885, 5.360153675079346, 5.449978828430176, 5.859875202178955, 5.862412452697754, 5.599879264831543, 5.520211458206177, 5.250281095504761, 5.401733636856079],
        [7.199877977371216, 6.3499486446380615, 7.399947166442871, 8.014953136444092, 7.050033330917358, 7.014585256576538, 7.799839019775391, 8.080129623413086, 6.56036376953125, 6.701298952102661],
        [7.5399885177612305, 7.529787540435791, 7.370052337646484, 7.260145902633667, 7.7199788093566895, 8.849814176559448, 7.620048999786377, 8.149760007858276, 9.119993448257446, 8.155161619186401],
        [10.389974117279053, 8.709822177886963, 9.040137529373169, 8.119767427444458, 8.669618844985962, 8.84520411491394, 8.769750833511353, 8.180006265640259, 8.920428991317749, 9.580013751983643]]
data = np.asarray(data)
force_means = np.mean(data, axis=1)
std = np.std(data, axis=1)

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, opt_means, width, label='Static Planning')
rects2 = ax.bar(x + width / 2, force_means, width, yerr=std, align='center', ecolor='black', capsize=10, label='Reactive Planning')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Number of quadcopters on circle')
ax.set_ylabel('Time until completion (s)')
ax.set_xticks(x)
ax.yaxis.grid(True)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        height = round(height, 1)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

fig.tight_layout()

SAVE = True
if SAVE:
    plt.savefig(sys.path[0] + "/circle_completion_comparison.pdf", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=0,
                frameon=None, metadata=None)
else:
    plt.show()
