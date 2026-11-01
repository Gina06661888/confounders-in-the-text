"""Draw the four-step proposal workflow; no model training or data access."""
from pathlib import Path
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"] = "none"  # Keep labels editable and searchable.
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[1]

def main():
    fig,ax=plt.subplots(figsize=(15.5,5.0))
    ax.set_xlim(0,16);ax.set_ylim(0,5);ax.axis('off')
    titles=['1  Data preparation','2  Embedding engine','3  Identification engine','4  Estimation engine']
    bodies=[
      'Extract and clean Item 1\n\nMeasure competition language T\n\nLink SEC dates and Compustat\n\nAlign one report-period row',
      'Encode retained paragraphs\n\nMiniLM  |  Llama  |  OpenAI\n\nAverage paragraph vectors\nand L2 normalize\n\nReport representation H',
      'Learn adjustment representation Z\n\nPredict outcome from Z, W, T\n\nAdversarial objective:\nreduce prediction of T from Z\n\nCompare with NoAdv',
      'Company-disjoint cross-fitting\n\nRidge / random-forest nuisances\n\nResidual-on-residual regression\n\nEffect estimates and diagnostics',
    ]
    for i,(title,body) in enumerate(zip(titles,bodies)):
        x=0.15+4*i
        ax.add_patch(FancyBboxPatch((x,0.65),3.65,3.55,boxstyle='round,pad=0.03,rounding_size=0.10',facecolor='#F2F6F9',edgecolor='#25465E',linewidth=1.5))
        ax.text(x+1.825,4.48,title,ha='center',va='center',fontsize=12,fontweight='bold',color='#17324D')
        ax.text(x+1.825,2.42,body,ha='center',va='center',fontsize=10.5,linespacing=1.30)
        if i<3:ax.add_patch(FancyArrowPatch((x+3.72,2.42),(x+3.98,2.42),arrowstyle='-|>',mutation_scale=16,color='#25465E',linewidth=1.5))
    fig.text(0.5,0.02,'Figure 1. Workflow of Generative AI–Assisted Causal Inference',ha='center',fontsize=13,fontweight='bold')
    out=ROOT/'outputs/figures';out.mkdir(parents=True,exist_ok=True)
    for ext in ['png','pdf','svg']:
        buf=BytesIO();fig.savefig(buf,format=ext,dpi=300,bbox_inches='tight',facecolor='white')
        (out/f'Figure1_Workflow.{ext}').write_bytes(buf.getvalue())
    plt.close(fig)

if __name__=='__main__':main()
