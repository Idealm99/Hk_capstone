// 이미지 업로드 및 출력
const imageUpload = document.getElementById('imageUpload');
const uploadedImage = document.getElementById('uploadedImage');

imageUpload.addEventListener('change', (e) => {
  const imageFile = e.target.files[0];
  if (imageFile) {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImage.src = e.target.result;
    };
    reader.readAsDataURL(imageFile);
  }
});

async function start() {
    try {
      await setupCamera();
      const stream = video.srcObject;
      faceMesh.send({ image: stream });
    } catch (error) {
      console.error('웹캠 액세스 권한이 거부되었습니다.', error);
      alert('웹캠 사용을 허용해야 합니다.');
    }
  }
  
// 헤어스타일 추천 버튼 클릭 이벤트 처리
const recommendHairstyleBtn = document.getElementById('recommendHairstyle');
const resultDiv = document.getElementById('result');

recommendHairstyleBtn.addEventListener('click', () => {
  if (uploadedImage.src) {
    resultDiv.innerHTML = '분석 중...';
    
    // 이미지 데이터 전송
    fetch('/calculate_face_ratios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: uploadedImage.src })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = '얼굴이 감지되지 않았습니다. 다른 이미지를 업로드해주세요.';
      } else {
        console.log('Face Ratios:', data);
        
        // 결과를 페이지에 출력
        resultDiv.innerHTML = `
          <h3>얼굴 비율 분석 결과:</h3>
          <p>상안부 비율: ${(data.upperFaceRatio * 100).toFixed(2)}%</p>
          <p>중안부 비율: ${(data.middleFaceRatio * 100).toFixed(2)}%</p>
          <p>하안부 비율: ${(data.lowerFaceRatio * 100).toFixed(2)}%</p>
        `;
        
        // 여기에서 계산된 비율을 사용하여 헤어스타일 추천 로직을 구현합니다.
      }
    })
    .catch(error => {
      console.error('Error:', error);
      resultDiv.innerHTML = '분석 중 오류가 발생했습니다.';
    });
  } else {
    alert('이미지를 업로드해주세요.');
  }
});