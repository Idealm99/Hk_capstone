from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import base64
import numpy as np

app = Flask(__name__)

@app.route('/calculate_face_ratios', methods=['POST'])
def calculate_face_ratios():
    # 이미지 데이터 받기
    image_data = request.json['image']
    
    # 이미지 디코딩
    image_data = base64.b64decode(image_data.split(',')[1])
    image_np = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    # MediaPipe Face Mesh 초기화
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)
    
    # 얼굴 랜드마크 검출
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        
        # 얼굴 비율 계산 함수
        def calculate_ratio(landmarks):
            # 상안부, 중안부, 하안부 랜드마크 인덱스
            upperFaceLandmarks = [10, 67, 297, 288, 109]
            middleFaceLandmarks = [195, 2, 416, 359, 267]
            lowerFaceLandmarks = [152, 149, 176, 400, 377]
            
            # 랜드마크 좌표 추출
            extractCoords = lambda i: [landmarks[i].x, landmarks[i].y, landmarks[i].z]
            
            # 랜드마크 좌표의 평균 계산
            calculateAverage = lambda coords: [sum(x) / len(coords) for x in zip(*coords)]
            
            upperFaceAverage = calculateAverage(map(extractCoords, upperFaceLandmarks))
            middleFaceAverage = calculateAverage(map(extractCoords, middleFaceLandmarks))
            lowerFaceAverage = calculateAverage(map(extractCoords, lowerFaceLandmarks))
            
            # 상안부, 중안부, 하안부의 길이 계산
            calculateDistance = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
            
            upperFaceLength = calculateDistance(upperFaceAverage, middleFaceAverage)
            middleFaceLength = calculateDistance(middleFaceAverage, lowerFaceAverage)
            lowerFaceLength = calculateDistance(lowerFaceAverage, upperFaceAverage)
            
            totalLength = upperFaceLength + middleFaceLength + lowerFaceLength
            
            # 비율 계산
            upperFaceRatio = upperFaceLength / totalLength
            middleFaceRatio = middleFaceLength / totalLength
            lowerFaceRatio = lowerFaceLength / totalLength
            
            return {
                'upperFaceRatio': upperFaceRatio,
                'middleFaceRatio': middleFaceRatio,
                'lowerFaceRatio': lowerFaceRatio
            }
        
        face_ratios = calculate_ratio(landmarks)
        
        return jsonify(face_ratios)
    else:
        return jsonify({'error': 'No face detected'})

if __name__ == '__main__':
    app.run()