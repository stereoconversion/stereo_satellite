import os
import glob
from PIL import Image, ImageFont, ImageDraw

orig_images = glob.glob(r'Original slices/orig_*.bmp')  # Obtained from the 24fps video using: ffmpeg -i 5Ok1A1fSzxY.mp4 "Original slices/orig_%04d.bmp"

def crop_image(input_filename):
    frame_number = int(os.path.basename(input_filename).split('_')[1].split('.')[0])
    
    output_A_filename = os.path.join(os.path.dirname(__file__),'Split',os.path.basename(input_filename).rsplit('.')[0]+'A'+'.bmp')
    output_B_filename = os.path.join(os.path.dirname(__file__),'Split',os.path.basename(input_filename).rsplit('.')[0]+'B'+'.bmp')

    with open(r'Split/frame_sequences.txt','a') as f:
        for i in range(1):
            f.write(f"file '{os.path.basename(output_A_filename)}'\n")
            f.write(f"file '{os.path.basename(output_B_filename)}'\n")

    
    if not(os.path.isfile(output_A_filename)) and not(os.path.isfile(output_B_filename)):
        img = Image.open(input_filename)

        left, upper, right, lower = 21-3, 0, 21-3+600, 720 # The +- 3 is to center the stereo view's height on the airplane's height
        cropped_img = img.crop((left, upper, right, lower))
        annotated_img = annotate_img(cropped_img, annotation_text=f"Frame {frame_number:04d} L from video 5Ok1A1fSzxY (approx t={frame_number/24:.2f}s)")
        annotated_img.save(output_A_filename)
   
        left, upper, right, lower = 661+3, 0, 661+3+600, 720
        cropped_img = img.crop((left, upper, right, lower))
        annotated_img = annotate_img(cropped_img, annotation_text=f"Frame {frame_number:04d} R from video 5Ok1A1fSzxY (approx t={frame_number/24:.2f}s)")
        annotated_img.save(output_B_filename)
    
    
    return # The output slices are then to be merged with: ffmpeg -f concat -r 48 -i Split/frame_sequences.txt -crf 10 -vf fps=48,format=yuv420p Output.mp4

def annotate_img(input_img, annotation_text):
    font_size = 14
    font = ImageFont.truetype("consola.ttf", font_size)
    
    padding_height = 5
    text_height = 12
    annotated_img = Image.new("RGB", (input_img.width, input_img.height + text_height + 2*padding_height))
    annotated_img.paste(input_img, (0, 0))
    
    draw = ImageDraw.Draw(annotated_img)
    text_position = (5, input_img.height + padding_height)
    text_color = (255, 255, 255)
    draw.text(text_position, annotation_text, font=font, fill=text_color)
    return annotated_img

if __name__ == "__main__":
    # Blanks out the frame sequence file
    with open(r'Split/frame_sequences.txt','w') as f:
        f.write("")

    for input_filename in orig_images:
        crop_image(input_filename)