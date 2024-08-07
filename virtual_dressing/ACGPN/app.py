from flask import Flask, flash, request, redirect, url_for, render_template, send_file
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok
from predict_pose import generate_pose_keypoints
import base64
import io
import json
import subprocess
import gdown
import numpy as np
from PIL import Image
import IPython
import gdown
import os
import sys
import time


app = Flask(__name__)

UPLOAD_FOLDER_1 = 'inputs/img'
UPLOAD_FOLDER_2 = 'inputs/cloth'

app.secret_key = "yashashree"
app.config['UPLOAD_FOLDER_1'] = UPLOAD_FOLDER_1
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.debug = True
run_with_ngrok(app)

directories_to_clear = [
    'Data_preprocessing/test_color',
    'Data_preprocessing/test_colormask',
    'Data_preprocessing/test_edge',
    'Data_preprocessing/test_img',
    'Data_preprocessing/test_label',
    'Data_preprocessing/test_mask',
    'Data_preprocessing/test_pose',
    'inputs/cloth',
    'inputs/img',
    'results/test/try-on',
    'results/test/refined_cloth',
    'results/test/warped_cloth'
]

# Function to remove files from directories
def remove_files_from_directories(directories):
    for directory in directories:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error while deleting {file_path}: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/women')
def women():
    return render_template('women.html')

@app.route('/result', methods=['POST'])
def result():
    # Check if the request contains files
    if 'image1' not in request.files or 'image2' not in request.files:
        return 'No file(s) selected'
    
    # Delete all the previous results 
    remove_files_from_directories(directories_to_clear)
    print("All the previous results have been cleared!")

    # Get the files from the request
    image1 = request.files['image1']
    image2 = request.files['image2']

    # Save the images to the UPLOAD_FOLDER
    filename1 = secure_filename(image1.filename)
    filename2 = secure_filename(image2.filename)
    image1.save(os.path.join(app.config['UPLOAD_FOLDER_1'], filename1))
    image2.save(os.path.join(app.config['UPLOAD_FOLDER_2'], filename2))

    cloth_name = '000001_1.png'
    cloth_path = os.path.join('inputs/cloth', sorted(os.listdir('inputs/cloth'))[0])
    cloth = Image.open(cloth_path)
    cloth = cloth.resize((192, 256), Image.BICUBIC).convert('RGB')
    cloth.save(os.path.join('Data_preprocessing/test_color', cloth_name))
    subprocess.call('cd U-2-Net', shell=True)
    subprocess.call('pwd', shell=True)
    print("---------------Executed- success------")
    sys.path.append('/content/drive/MyDrive/Major_Project/ACGPN/U-2-Net')
    subprocess.call('pwd', shell=True)
    import u2net_run
    import u2net_load
    u2net = u2net_load.model(model_name = 'u2netp')
    subprocess.call('cd ..', shell=True)

    u2net_run.infer(u2net, 'Data_preprocessing/test_color', 'Data_preprocessing/test_edge')

    start_time = time.time()
    img_name = '000001_0.png'
    img_path = os.path.join('inputs/img', sorted(os.listdir('inputs/img'))[0])
    img = Image.open(img_path)
    img = img.resize((192,256), Image.BICUBIC)

    img_path = os.path.join('Data_preprocessing/test_img', img_name)
    img.save(img_path)
    resize_time = time.time()
    print('Resized image in {}s'.format(resize_time-start_time))

    subprocess.call("python3 Self-Correction-Human-Parsing-for-ACGPN/simple_extractor.py --dataset 'lip' --model-restore 'lip_final.pth' --input-dir 'Data_preprocessing/test_img' --output-dir 'Data_preprocessing/test_label'", shell=True)
    parse_time = time.time()
    print('Parsing generated in {}s'.format(parse_time-resize_time))

    pose_path = os.path.join('Data_preprocessing/test_pose', img_name.replace('.png', '_keypoints.json'))
    generate_pose_keypoints(img_path, pose_path)
    pose_time = time.time()
    print('Pose map generated in {}s'.format(pose_time-parse_time))


    subprocess.call("rm -rf Data_preprocessing/test_pairs.txt", shell=True)
    with open('Data_preprocessing/test_pairs.txt','w') as f:
        f.write('000001_0.png 000001_1.png')

    subprocess.call("python test.py", shell=True)
    img_load = Image.open('results/test/try-on/000001_0.png')
    result_grid = np.array(img_load)
    img = Image.fromarray(result_grid)
    print("Test Executed")
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    encoded_string = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
    # Return a success message
    print("Image Sent")
    return render_template('result.html',result_img_url=f"data:image/png;base64,{encoded_string}")



@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# if __name__ == "__main__":
# app.port = 8000
app.run()
