import argparse
import shutil
from pathlib import Path

## Usage
# python3 temporalDsTool.py {path_to_ply_dir} {path_to_save} {num_of_frame}

def myKey(text):
    return int(text.split('frame')[-1])

def downsampleFrames(ply_dir,save_dir,num_of_frame):
    save_dir.mkdir(parents=True,exist_ok=True)

    ply_filename_list = sorted([i.stem for i in ply_dir.glob("frame*.ply")])
    ply_filename_list.sort(key=myKey)
    print(f"From {len(ply_filename_list)} frames downsample to {num_of_frame} frames")
    if len(ply_filename_list) < num_of_frame:
        print("The frames are not enough.")
    elif len(ply_filename_list) == num_of_frame:
        print("There are nothing have to done.")
    else:
        sliced_list = ply_filename_list[0:-1:int(len(ply_filename_list)/10)]
        for filename in sliced_list:
            shutil.copy2(ply_dir/f'{filename}.ply', save_dir)
        print("Done")


if __name__ == "__main__":
    # do not modify
    # +++++++++++++++++++++++++++++++++ #
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_ply_dir", type=str, 
                        help="Path to the ply dir")
    parser.add_argument("path_to_save", type=str, 
                        help="Path to save ply file")
    parser.add_argument("num_of_frame", type=int, 
                        help="Downsample to # of frame")
    
    args = parser.parse_args()
    path_to_ply_dir = args.path_to_ply_dir
    path_to_save = args.path_to_save
    num_of_frame = args.num_of_frame
    # +++++++++++++++++++++++++++++++++ #

    downsampleFrames(Path(path_to_ply_dir),Path(path_to_save),num_of_frame)
    