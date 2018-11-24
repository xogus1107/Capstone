#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;
/*
void sharpen2D(const cv::Mat &image, cv::Mat &result) {
	cv::Mat kernel(3, 3, CV_32F, cv::Scalar(0));
	// 커널 생성(모든 값을 0으로 초기화)
	kernel.at<float>(1, 1) = 5.0; // 커널 값에 할당
	kernel.at<float>(0, 1) = -1.0;
	kernel.at<float>(2, 1) = -1.0;
	kernel.at<float>(1, 0) = -1.0;
	kernel.at<float>(1, 2) = -1.0;

	cv::filter2D(image, result, image.depth(), kernel);
	// 영상 필터링
}
*/
int main(int argc, char** argv) {
	Mat bilateral = imread("picture.png", 1);
	Mat b = bilateral.clone();
	Mat gaussian = bilateral.clone();
	Mat median = bilateral.clone();
	Mat result, result1, result2, result3,result4;
	Mat a, c, d,e;
	imshow("original image", bilateral);

	Rect rect(98, 267, 390, 390);
	Mat subImage = bilateral(rect);

	
	blur(b, result, Size(5, 5));
	//imshow("blur result", result);

	GaussianBlur(b, result1, Size(5, 5), 1.5, 1.5);
	//imshow("GaussianBlur result", result1);
	
	medianBlur(b, result2, 7);
	//imshow("medianBlur result", result2);

	//bilateralFilter(result2, result3, 10, 50, 50);
 	//imshow("max result", result3);
	
	bilateralFilter(b, result3, 10, 50, 50);
	//imshow("bilateralFilter result", result4);
	
	//Mat imageROI = bilateral(Rect(98, 267, 390, 390));
	//addWeighted(imageROI, 1.0, result4, 0.3, 0., imageROI);
	//imshow("imageROI", bilateral);
	sharpen2D(result, a);
	imshow("blur", a);
	sharpen2D(result1, e);
	imshow("gaussian", e);
	sharpen2D(result2, c);
	imshow("median", c);
	sharpen2D(bilateral, d);
	imshow("result", d);

	/*
	bilateralFilter (1, 2, 3, 4, 5);

	argument 1 : Source image
	argument 2 : Destination image
	argument 3 : the diameter of each pixel neighborhood
	argument 4 : Standard deviation in the color space
	argument 5 : Standard deviation in the coordinate space
	*/


	waitKey(0);
	return 0;
}
