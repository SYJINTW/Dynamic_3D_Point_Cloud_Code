# Tools for dataset

We provide three tools to downsample the point cloud sequences in temporal and spatial domain, and a tool to scale the point cloud object.

**Temporal downsampling tool** is a tool to downsample the frames to a specific number of frames. 
The input of the tool will be the path to the ply file directory, the path going to store the downsampling results, and an integer number which is the target downsample expected frame number. 
In this tool, we just downsample the frame in a simple method, which is sampled in the same step according to the frames' order.

**Spatial downsampling tool** is about downsampling the resolution which means downsampling the vertices number. 
The input of the tool will be the path to the ply file directory, the path going to store the downsampling results, and an integer number which is the target expected vertices number. 
In this tool, we downsample the vertices randomly which is the simplest way to implement, and after downsampling, the characteristic of point-to-point matching will still exist. 
In the future, we plan to release the voxelized downsample method to our dataset, which is able to make our dataset more realistic.

**Object scaling tool** is used for adjusting the size of objects in point cloud data. 
The input of the tool will be the path to the ply file directory, the path going to store the downsampling results, and a float number which is the expected scaling factor.
This tool scales the object with the origin (0,0,0) as the center.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary package.

### Temporal downsampling tool
```bash
# nothing is needed except the built-in module
```

### Spatial downsampling tool
```bash
pip install plyfile
```

### Object scaling tool
```bash
pip install plyfile
```

## Usage

### Temporal downsampling tool
```bash
python3 temporalDsTool.py {path_to_ply_dir} {path_to_save} {num_of_frame}
```
- `path_to_ply_dir` is the path to the directory that store all the .ply file.
- `path_to_save` is the path to the directory to save the output .ply file.
- `num_of_frame` is an *integer* which is the expected frame number.


### Spatial downsampling tool
```bash
python3 spatialDsTool.py {path_to_ply_dir} {path_to_save} {num_of_point} {random_seed}
```

- `path_to_ply_dir` is the path to the directory that store all the .ply file.
- `path_to_save` is the path to the directory to save the output .ply file.
- `num_of_point` is an *integer* which is the expected point number.
- `random_seed` is an *integer* which control the subset of the chosen points. 

### Object scaling tool
```bash
XXX
```