import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11})
labels=["AI-READI","AI-READI Vision","AI-READI MoCA"]
concepts=[266,47,30]; elements=[389,69,30]
blue,orange="#2A7AD5","#EB6936"
fig,ax=plt.subplots(figsize=(10,4.3),dpi=300)
h=0.36; ys=[2,1,0]
for y,c,e in zip(ys,concepts,elements):
    ax.barh(y+h/2+0.01,c,h,color=blue,edgecolor="white")
    ax.barh(y-h/2-0.01,e,h,color=orange,edgecolor="white")
    ax.text(c+5,y+h/2+0.01,str(c),va="center",fontsize=11)
    ax.text(e+5,y-h/2-0.01,str(e),va="center",fontsize=11)
ax.set_yticks(ys); ax.set_yticklabels(labels,fontsize=12)
ax.set_xlim(0,430); ax.set_xlabel("Count",color="#444")
ax.xaxis.grid(True,color="#e3e3e3"); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#aaa"); ax.tick_params(axis="y",length=0); ax.tick_params(axis="x",colors="#444")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=blue,label="Distinct custom concepts (n = 343)"),Patch(color=orange,label="Mapped data elements (n = 488)")],loc="lower right",frameon=False,fontsize=11)
plt.tight_layout()
fig.savefig("Figure3_custom_concepts.png",dpi=300)
fig.savefig("Figure3_custom_concepts.pdf")
fig.savefig("Figure3_custom_concepts.tiff",dpi=300,pil_kwargs={"compression":"tiff_lzw"})
