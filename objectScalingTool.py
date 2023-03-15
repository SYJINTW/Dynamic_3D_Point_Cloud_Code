from pathlib import Path
import open3d as o3d
from plyfile import PlyData, PlyElement
import numpy as np
import pandas as pd
import json
import argparse
import shutil

scaleFactor = 100

def AddPlyHeader(saveFilePath, numOfVertex):
    header = 'ply\n'
    header = header + f'format ascii 1.0\n' \
                    + f'comment made by Yuan-Chun Sun\n' \
                    + f'element vertex {numOfVertex}\n' \
                    + f'property uchar obj\n' \
                    + f'property int idx\n' \
                    + f'property float x\n' \
                    + f'property float y\n' \
                    + f'property float z\n' \
                    + f'property uchar red\n' \
                    + f'property uchar green\n' \
                    + f'property uchar blue\n' \
                    + f'end_header\n'
    with open(str(saveFilePath),"w") as f:
        f.write(header)

def AddPlyBody(saveFilePath,datas):
    body = ''
    for data in datas:
        # [x, y, z, u, v, r, g, b, idx, objName]
        body = body + f"{int(data[0])} {int(data[1])} {data[2]} {data[3]} {data[4]} {int(data[5])} {int(data[6])} {int(data[7])} \n"
    with open(str(saveFilePath),"a") as f:
        f.write(body)
    print(f'done {saveFilePath}')

def scalePointCloud(file_path, save_file_path):
    # obj idx x y z red green blue
    ply_data = PlyData.read(file_path)
    data = ply_data.elements[0].data
    data_pd = pd.DataFrame(data)
    data_pd['x'] = data_pd['x'] * scaleFactor
    data_pd['y'] = data_pd['y'] * scaleFactor
    data_pd['z'] = data_pd['z'] * scaleFactor
    data_list = data_pd.values.tolist()

    AddPlyHeader(save_file_path, len(data_list))
    AddPlyBody(save_file_path, data_list)
    
if __name__ == "__main__":
    global scaleFactor
    # do not modify
    # +++++++++++++++++++++++++++++++++ #
    parser = argparse.ArgumentParser()
    parser.add_argument("projName", type=str, 
                        help="Project Name (Object Name)")
    parser.add_argument("keyword", type=str, 
                        help="Keyword (Movement Name)")
    parser.add_argument("scaleFactor", type=int, 
                        help="Scale factor")
    # parser.add_argument("endFrame", type=int, 
    #                     help="End Frame")
    # parser.add_argument("step", type=int, 
    #                     help="Step Frame")
    args = parser.parse_args()
    
    projName = args.projName
    keyword = args.keyword
    scaleFactor = args.scaleFactor
    newProjName = f"{projName}_scale"

    # startFrame = args.startFrame
    # endFrame = args.endFrame
    # step = args.step
    # captureFrame = [i for i in range(startFrame,endFrame,step)]

    # do not modify
    # +++++++++++++++++++++++++++++++++ #
    projDir = Path('..')/f'{projName}'
    inputDir = projDir/f'output_{keyword}_ply'
    inputDir_base = inputDir/'base'
    inputDir_light = inputDir/'light'

    saveDir = Path('..')/f'{newProjName}'/f'output_{keyword}_ply'
    saveDir.mkdir(parents=True,exist_ok=True)
    saveDir_base = saveDir/f'base'
    saveDir_base.mkdir(parents=True,exist_ok=True)
    saveDir_light = saveDir/f'light'
    saveDir_light.mkdir(parents=True,exist_ok=True)
    
    with open(str(inputDir/'para.json')) as json_f:
        json_array = json.load(json_f)
        objectNames = json_array["objectNames"]
        numOfObject = len(objectNames)
    shutil.copy2(inputDir/'para.json', saveDir)
    # +++++++++++++++++++++++++++++++++ #

    for objectName in objectNames:
        # base
        input_file_dir = inputDir_base/objectName
        output_file_dir = saveDir_base/objectName
        output_file_dir.mkdir(parents=True,exist_ok=True)

        for file_path in input_file_dir.glob('*.ply'):
            save_file_path = output_file_dir/file_path.name
            scalePointCloud(file_path, save_file_path)

        # light
        input_file_dir = inputDir_light/objectName
        output_file_dir = saveDir_light/objectName
        output_file_dir.mkdir(parents=True,exist_ok=True)

        for file_path in input_file_dir.glob('*.ply'):
            save_file_path = output_file_dir/file_path.name
            scalePointCloud(file_path, save_file_path)
