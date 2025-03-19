# coding:utf-8
from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import detect_tools as tools
# import paddleocr
import numpy as np
from PIL import ImageFont
import io

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 OCR 模型
# cls_model_dir = 'ch_ppocr_mobile_v2.0_cls_infer'
# rec_model_dir = 'ch_PP-OCRv4_rec_infer'
# ocr = paddleocr.PaddleOCR(use_angle_cls=False, lang="ch", det=False, cls_model_dir=cls_model_dir, rec_model_dir=rec_model_dir)

# 初始化 YOLO 模型
path = 'best.pt'
model = YOLO(path, task='detect')

def get_license_result(ocr, image):
    """
    识别车牌号码
    :param ocr: PaddleOCR 实例
    :param image: 车牌图像
    :return: 车牌号码, 置信度
    """
    result = ocr.ocr(image, cls=True)[0]
    if result:
        license_name, conf = result[0][1]
        if '·' in license_name:
            license_name = license_name.replace('·', '')
        return license_name, conf
    else:
        return None, None

@app.route('/detect', methods=['POST'])
def detect_license_plate():
    """
    车牌检测与识别 API
    """
    # 检查是否有文件上传
    print("Request files:", request.files)

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # 读取上传的图片
    file = request.files['file']
    image_bytes = file.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # 使用 YOLO 检测车牌
    results = model(image)[0]
    location_list = results.boxes.xyxy.tolist()

    # 如果没有检测到车牌
    if len(location_list) == 0:
        return jsonify({"message": "未识别到车牌"}), 200

    # 截取车牌区域并识别
    license_imgs = []
    for each in location_list:
        x1, y1, x2, y2 = list(map(int, each))
        cropImg = image[y1:y2, x1:x2]
        license_imgs.append(cropImg)

    # 识别车牌号码
    # license_results = []
    # for each in license_imgs:
    #     license_num, conf = get_license_result(ocr, each)
    #     license_results.append({
    #         "license_number": license_num if license_num else "无法识别",
    #         "confidence": float(conf) if conf else 0.0
    #     })
    print(license_imgs)

    # 返回结果
    return jsonify({
        "detected_plates": '识别到车牌区域'

        # "detected_plates": license_results
    })

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=5000, debug=True)