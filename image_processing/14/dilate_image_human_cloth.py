import numpy as np
import os, argparse
from tqdm import tqdm
import cv2

if __name__ == '__main__':
    """
    人物パース画像から服部分を膨張させる。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_image_human_dir", type=str)
    parser.add_argument("in_image_human_parsing_dir", type=str)
    parser.add_argument("out_image_dir", type=str)
    parser.add_argument('--width', type=int, default=192 )
    parser.add_argument('--height', type=int, default=256 )
    parser.add_argument('--dilate_kernel_size', type=int, default=12 )
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if( args.debug ):
        for key, value in vars(args).items():
            print('%s: %s' % (str(key), str(value)))

    if not os.path.isdir(args.out_image_dir):
        os.mkdir(args.out_image_dir)

    image_human_names = sorted( [f for f in os.listdir(args.in_image_human_dir) if f.endswith(('.jpg','.jpeg','.png','.bmp'))] )
    image_human_parsing_names = sorted( [f for f in os.listdir(args.in_image_human_parsing_dir) if f.endswith(('.jpg','.jpeg','.png','.bmp'))] )

    for human_name in tqdm(image_human_names):
        human_img = cv2.imread(os.path.join(args.in_image_human_dir, human_name ))
        human_parsing_img = cv2.imread(os.path.join(args.in_image_human_parsing_dir, human_name ))
        human_parsing_img = cv2.cvtColor(human_parsing_img, cv2.COLOR_RGB2GRAY)

        #------------------
        # 背景を抽出
        #------------------
        human_parsing_back_np = (human_parsing_img == 0).astype(np.float32)
        human_parsing_back_np = cv2.cvtColor(human_parsing_back_np, cv2.COLOR_GRAY2RGB)
        new_human_img = human_img * human_parsing_back_np
        
        #------------------
        # 服以外の部分を抽出
        #------------------
        human_parsing_agnotic_np = \
            (human_parsing_img == 1).astype(np.float32) + \
            (human_parsing_img == 2).astype(np.float32) + \
            (human_parsing_img == 3).astype(np.float32) + \
            (human_parsing_img == 4).astype(np.float32) + \
            (human_parsing_img == 8).astype(np.float32) + \
            (human_parsing_img == 9).astype(np.float32) + \
            (human_parsing_img == 10).astype(np.float32) + \
            (human_parsing_img == 11).astype(np.float32) + \
            (human_parsing_img == 12).astype(np.float32) + \
            (human_parsing_img == 13).astype(np.float32) + \
            (human_parsing_img == 14).astype(np.float32) + \
            (human_parsing_img == 15).astype(np.float32) + \
            (human_parsing_img == 16).astype(np.float32) + \
            (human_parsing_img == 17).astype(np.float32) + \
            (human_parsing_img == 18).astype(np.float32) + \
            (human_parsing_img == 19).astype(np.float32)

        human_parsing_agnotic_np = cv2.cvtColor(human_parsing_agnotic_np, cv2.COLOR_GRAY2RGB)
        new_human_img += human_img * human_parsing_agnotic_np
        
        #------------------
        # 人物パース画像から cloth 部分を抽出
        #------------------
        human_parsing_cloth_np = \
            (human_parsing_img == 5).astype(np.float32) + \
            (human_parsing_img == 6).astype(np.float32) + \
            (human_parsing_img == 7).astype(np.float32)

        # 畳み込み用カーネルを設定
        kernel = np.ones((args.dilate_kernel_size, args.dilate_kernel_size), np.uint8)

        # cv2.dilate() でマスク画像を膨張
        human_parsing_cloth_np = cv2.dilate(human_parsing_cloth_np, kernel )

        #human_parsing_cloth_np *= 255
        #print( "human_parsing_cloth_np.shape :", human_parsing_cloth_np.shape )
        #human_parsing_agnotic_np = cv2.cvtColor(human_parsing_agnotic_np, cv2.COLOR_GRAY2RGB)
        #new_human_img += human_img * human_parsing_cloth_np

        cv2.imwrite(os.path.join(args.out_image_dir, human_name.split(".")[0] + ".png" ), new_human_img)