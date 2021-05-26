import cv2
import numpy as np

def unpack_png_to_float(png):
    depthImageUnit = 0.00001
    png = png.astype(float)
    depth = (png[:, :, 0] + png[:, :, 1] * 256 +
             png[:, :, 2] * 256 * 256) * depthImageUnit
    return depth


def pack_float_to_bmp_bgra(depth):
    m, e = np.frexp(depth)
    m = (m * (256**3)).astype(np.uint64)
    bmp = np.zeros((*depth.shape[:2], 4), np.uint8)
    bmp[:, :, 0] = (e + 128).astype(np.uint8)
    bmp[:, :, 1] = np.right_shift(np.bitwise_and(m, 0x00ff0000), 16)
    bmp[:, :, 2] = np.right_shift(np.bitwise_and(m, 0x0000ff00), 8)
    bmp[:, :, 3] = np.bitwise_and(m, 0x000000ff)
    return bmp


def unpack_bmp_bgra_to_float(bmp):
    b = bmp[:, :, 0].astype(np.int32)
    g = bmp[:, :, 1].astype(np.int32) << 16
    r = bmp[:, :, 2].astype(np.int32) << 8
    a = bmp[:, :, 3].astype(np.int32)
    depth = np.ldexp(1.0, b -
                     (128 + 24)) * (g + r + a + 0.5).astype(np.float32)
    return depth


def unpack_bmp_bgr_to_float(bmp):
    b = bmp[:, :, 0].astype(np.int32)
    g = bmp[:, :, 1].astype(np.int32) << 16
    r = bmp[:, :, 2].astype(np.int32) << 8
    depth = np.ldexp(1.0, b - (128 + 24)) * (g + r + 0.5).astype(np.float32)
    return depth


def convert_depth_to_coords(raw_depth, cam_params):
    h, w = raw_depth.shape[:2]

    # convert depth to 3d coord
    xs, ys = np.meshgrid(range(w), range(h))

    z = raw_depth
    dist_x = cam_params['pix_x'] * (xs - cam_params['center_x'])
    dist_y = -cam_params['pix_y'] * (ys - cam_params['center_y'])
    xyz = np.vstack([(dist_x * z / cam_params['focal_length']).flatten(),
                     (dist_y * z / cam_params['focal_length']).flatten(),
                     -z.flatten()]).T.reshape((h, w, -1))
    return xyz

def dump_ply(filename, points, colors=None, faces=None):
    params = []
    minimum = 0.2

    arr_points = np.array(points)
    length = np.sum(np.where(np.abs(arr_points[:, 2]) > minimum, 1, 0))
    params.append(length)

    header = 'ply\n'
    header += 'format ascii 1.0\n'
    header += 'element vertex {:d}\n'
    header += 'property float x\n'
    header += 'property float y\n'
    header += 'property float z\n'
    header += 'property uchar red\n'
    header += 'property uchar green\n'
    header += 'property uchar blue\n'

    if faces is not None:
        params.append(len(faces))
        header += 'element face {:d}\n'
        header += 'property list uchar int vertex_indices \n'

    header += 'end_header\n'

    colors = colors if colors is not None else [[255, 255, 255]] * len(points)
    with open(filename, 'w') as f:
        f.write(header.format(*params))
        for p, color in zip(points, colors):
            if np.abs(p[2]) > minimum:
                data = (p[0], p[1], p[2], color[0], color[1], color[2])
                f.write('%f %f %f %u %u %u\n' % data)

        faces = faces if faces is not None else []
        for v in faces:
            data = (v[0], v[1], v[2])
            f.write('3 %d %d %d \n' % data)