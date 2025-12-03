import argparse
import cv2
import numpy as np
from imutils import perspective
from imutils import contours
import imutils


# 두 점 사이의 중간 지점 계산 함수
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# 실제 측정을 수행하는 함수
def measure(image_path, ref_width):
    # 이미지 읽기
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")

    # 원본 복사
    orig = image.copy()

    # 그레이스케일 & 블러
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # 엣지(윤곽) 검출
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # 컨투어(윤곽선) 찾기
    cnts = cv2.findContours(
        edged.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = imutils.grab_contours(cnts)

    # 왼쪽 → 오른쪽 순으로 정렬
    (cnts, _) = contours.sort_contours(cnts)

    pixels_per_metric = None

    # 각 컨투어에 대해 반복
    for c in cnts:
        # 너무 작은 노이즈는 무시
        if cv2.contourArea(c) < 100:
            continue

        # 회전된 최소 영역 사각형 (bounding box)
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # 점 순서를 (tl, tr, br, bl) 로 정렬
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box

        # bounding box를 원본에 그리기
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # 각 변의 중간 지점 계산
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # 세로/가로 길이 (픽셀 단위)
        dA = np.linalg.norm([tltrX - blbrX, tltrY - blbrY])  # 세로
        dB = np.linalg.norm([tlblX - trbrX, tlblY - trbrY])  # 가로

        # 첫 번째 contour = 기준 물체 (reference object)
        if pixels_per_metric is None:
            # ref_width: 기준 물체의 실제 가로 길이 (cm 또는 inch)
            pixels_per_metric = dB / ref_width

        # 실제 단위(cm 또는 inch)로 변환
        dimA = dA / pixels_per_metric
        dimB = dB / pixels_per_metric

        # 화면(이미지) 위에 길이 텍스트 표시
        cv2.putText(
            orig,
            "{:.2f}".format(dimA),
            (int(tltrX - 10), int(tltrY - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2,
        )

        cv2.putText(
            orig,
            "{:.2f}".format(dimB),
            (int(trbrX + 10), int(trbrY)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2,
        )

    return orig


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        required=True,
        help="측정할 이미지 경로 (예: images/sample.jpg)"
    )
    parser.add_argument(
        "--width",
        required=True,
        type=float,
        help="reference object 실제 가로 길이 (cm 또는 inch)"
    )

    args = parser.parse_args()

    # 실제 측정 실행
    result = measure(args.image, args.width)

    # 결과 이미지 저장
    output_path = "output/annotated_result.png"
    cv2.imwrite(output_path, result)
    print("Saved:", output_path)
