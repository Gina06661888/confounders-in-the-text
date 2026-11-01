"""Export the supplied proposal Figure 1 without redrawing its content."""
from pathlib import Path
from io import BytesIO
import base64
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'figures/Figure1_Workflow.png'

def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f'Proposal source image missing: {SOURCE}')
    target=ROOT/'outputs/figures';target.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_bytes()
    image=mpimg.imread(BytesIO(original),format='png')
    height,width=image.shape[:2]
    # Retain the original image bytes; no labels or geometry are redrawn.
    png=target/'Figure1_Workflow.png';shutil.copyfile(SOURCE,png)
    payload=base64.b64encode(original).decode('ascii')
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
         f'<title>Figure 1 Workflow of Generative AI Assisted Causal Inference</title>'
         f'<image width="{width}" height="{height}" xlink:href="data:image/png;base64,{payload}"/>'
         '</svg>')
    (target/'Figure1_Workflow.svg').write_text(svg,encoding='utf-8')
    fig=plt.figure(figsize=(width/100,height/100),dpi=100)
    ax=fig.add_axes([0,0,1,1]);ax.imshow(image);ax.axis('off')
    buf=BytesIO();fig.savefig(buf,format='pdf',dpi=100,pad_inches=0)
    (target/'Figure1_Workflow.pdf').write_bytes(buf.getvalue());plt.close(fig)
    for extension in ('png','pdf','svg'):print('Saved:',target/f'Figure1_Workflow.{extension}')

if __name__=='__main__':main()
