# Measuring Size of Objects with OpenCV (Team Project Edition)

이 프로젝트는 한 장의 이미지와 기준 물체(reference object) 하나만으로
다른 물체들의 실제 크기(가로/세로)를 추정하는 예제입니다.

OpenCV와 NumPy, imutils만 사용하며,
컨투어 검출 → 최소 영역 사각형 → 픽셀-당-길이(pixel-per-metric)를 구해
실제 단위(cm 또는 inch)로 변환합니다.

---

## Key Features

1. 이미지에서 객체 컨투어 자동 추출
2. `cv2.minAreaRect()` 를 이용한 회전된 최소 영역 사각형(bounding box) 계산
3. 각 변의 중간 지점(midpoint)을 이용한 가로/세로 길이 측정
4. 기준 물체(reference object)를 이용한 Pixel-Per-Metric(PPM) 보정
5. 모든 물체의 실제 크기를 cm / inch 단위로 추정
6. 결과 이미지를 파일로 저장 (bounding box + 길이 텍스트 overlay)
7. 커맨드라인 인자를 이용한 간단한 실행 방법 제공

---

## How It Works

1. 입력 이미지를 그레이스케일로 변환하고 블러를 적용합니다.
2. Canny 엣지 검출과 팽창/침식(dilate/erode)으로 윤곽선을 강조합니다.
3. 윤곽선(contours)을 찾고, 왼쪽에서 오른쪽 순으로 정렬합니다.
4. 첫 번째 유효한 컨투어를 기준 물체(reference object)로 사용합니다.
5. 기준 물체의 실제 가로 길이(예: 신용카드 8.56cm)를 알고 있으므로,
   - 기준 물체의 가로 픽셀 길이 / 실제 길이 = Pixel-Per-Metric
6. 나머지 물체들도 같은 비율로 환산하여 실제 가로/세로 길이를 계산합니다.
7. 계산된 값을 이미지 위에 텍스트로 표시하고, 결과 이미지를 `output/annotated_result.png` 로 저장합니다.

---

## Reference Object Examples

- 신용카드 (가로 8.56cm)
- 동전 (예: 0.955 inch)
- 자(ruler), 카드, AirPods 케이스 등

조건:
1. 실제 가로/세로 길이를 알고 있어야 하고
2. 이미지에서 쉽게 구분되는 물체이면 됩니다.

---

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy
- imutils

이 리포지토리에는 다음 파일이 포함됩니다.

- `requirements.txt`
  - 위 패키지들을 설치하기 위한 목록
- `src/measure.py`
  - 실제 측정 로직이 들어 있는 파이썬 코드
- `images/sample.jpg`
  - 기준 물체가 포함된 샘플 이미지
- `output/`
  - 결과 이미지가 저장될 폴더

---

## Running the Program (로컬에서 실행할 때)

> 아래 내용은 **GitHub 웹이 아니라, 나중에 내 컴퓨터(로컬)** 에서 테스트할 때 사용합니다.

1. 이 리포지토리를 로컬에 클론합니다.

   ```bash
   git clone https://github.com/yutaehwi/object-size-measurement-opencv
   cd object-size-measurement-opencv
윤수열
