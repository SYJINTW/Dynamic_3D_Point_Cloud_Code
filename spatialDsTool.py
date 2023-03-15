import argparse
import shutil
import random
import json
from pathlib import Path
from plyfile import PlyData, PlyElement

## Usage
# python3 spatialDsTool.py {path_to_ply_dir} {path_to_save} {num_of_point} {random_seed}

def AddPlyHeader(saveFilePath, numOfVertex):
    header = 'ply\n'
    header = header + f'format ascii 1.0\n' \
                    + f'comment made by Yuan-Chun Sun\n' \
                    + f'comment this file is about merging all the element\n' \
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
        body = body + f"{int(data[0])} {int(data[1])} {data[2]} {data[3]} {data[4]} {int(data[5])} {int(data[6])} {int(data[7])} \n"
    with open(str(saveFilePath),"a") as f:
        f.write(body)
    print(f'done {saveFilePath}')

def saveToPly(plySavePath:Path,results:list):
    AddPlyHeader(plySavePath,len(results))
    AddPlyBody(plySavePath,results)       

def myKey(text):
    return int(text.split('frame')[-1])

def downsampleFrames(ply_dir,save_dir,num_of_point,random_seed):
    save_dir.mkdir(parents=True,exist_ok=True)

    ply_filename_list = sorted([i.stem for i in ply_dir.glob("frame*.ply")])
    ply_filename_list.sort(key=myKey)
    base_ply_file_path = ply_dir/f'{ply_filename_list[0]}.ply'
    base_ply_data = PlyData.read(base_ply_file_path)
    base_data = base_ply_data.elements[0].data
    if len(base_data) < num_of_point:
        print("The frames are not enough.")
        return
    elif len(base_data) == num_of_point:
        print("There are nothing have to done.")
        return
    else:
        random.seed(random_seed)
        choose_idx_list = random.sample(range(len(base_data)),num_of_point)
        choose_idx_list = sorted(choose_idx_list)
        # save log
        with open(str(save_dir/"chosen_index.json"), "w") as json_f:
            json_data = {"chosen_idx_list": choose_idx_list,
                        "num_of_point": num_of_point,
                        "random_seed": random_seed}
            json.dump(json_data, json_f)

        print(f"From {len(base_data)} points downsample to {num_of_point} frames")
        for filename in ply_filename_list:
            ply_file_path = ply_dir/f'{filename}.ply'
            save_file_path = save_dir/f'{filename}.ply'
            ply_data = PlyData.read(ply_file_path)
            data = ply_data.elements[0].data
            chosen_data = []
            for idx in choose_idx_list:
                chosen_data.append(data[idx])
            saveToPly(save_file_path,chosen_data)
    print("Done")


if __name__ == "__main__":
    # do not modify
    # +++++++++++++++++++++++++++++++++ #
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_ply_dir", type=str, 
                        help="Path to the ply dir")
    parser.add_argument("path_to_save", type=str, 
                        help="Path to save ply file")
    parser.add_argument("num_of_point", type=int, 
                        help="Dowsample to # of point")
    parser.add_argument("random_seed", type=int, 
                        help="Random seed")
    
    args = parser.parse_args()
    path_to_ply_dir = args.path_to_ply_dir
    path_to_save = args.path_to_save
    num_of_point = args.num_of_point
    random_seed = args.random_seed
    # +++++++++++++++++++++++++++++++++ #

    downsampleFrames(Path(path_to_ply_dir),Path(path_to_save),num_of_point,random_seed)
    