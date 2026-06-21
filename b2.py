from abc import ABC, abstractmethod

class BaseLesson(ABC):
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code, title):
        self._lesson_code = lesson_code
        self._title = title.strip().upper()
        self.__duration_minutes = 0

    @property
    def lesson_code(self):
        return self._lesson_code

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value.strip().upper()

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    def set_duration(self, minutes):
        if minutes <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        self.__duration_minutes = minutes

    @abstractmethod
    def calculate_completion_score(self):
        pass

    @abstractmethod
    def update_content(self, new_data):
        pass

    @staticmethod
    def validate_lesson_code(lesson_code):
        return len(lesson_code) == 10 and lesson_code.startswith("LMS")

    @classmethod
    def update_base_points(cls, new_points):
        cls.base_completion_points = new_points

    def __add__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes


class VideoLesson(BaseLesson):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)
        self.video_quality = "1080p"
        self.view_count = 0

    def play_video(self):
        self.view_count += 1

    def calculate_completion_score(self):
        return self.base_completion_points + (self.duration_minutes * 0.5)

    def update_content(self, new_data):
        if isinstance(new_data, str):
            self.video_quality = new_data
        elif isinstance(new_data, (int, float)):
            self.set_duration(new_data)


class CodingChallenge(BaseLesson):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)
        self.number_of_testcases = 5
        self.difficulty_multiplier = 1.5

    def calculate_completion_score(self):
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        if isinstance(new_data, int):
            if new_data <= 0:
                raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
            self.number_of_testcases = new_data
        elif isinstance(new_data, float):
            self.set_duration(new_data)


class HybridAssessment(VideoLesson, CodingChallenge):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)
        CodingChallenge.__init__(self, lesson_code, title)

    def calculate_completion_score(self):
        video_score = VideoLesson.calculate_completion_score(self)
        challenge_score = CodingChallenge.calculate_completion_score(self)
        return video_score + challenge_score

    def update_content(self, new_data):
        if isinstance(new_data, int):
            if new_data <= 0:
                raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
            self.number_of_testcases = new_data
        else:
            super().update_content(new_data)


class AWSS3StorageService:
    def upload_lesson(self, lesson):
        print("[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        print("Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")


class GoogleCloudStorageService:
    def upload_lesson(self, lesson):
        print("[Hệ thống Google Cloud]: Kiểm tra token bảo mật OAuth2...")
        print("Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Đã lưu trữ cấu trúc bài giảng {lesson.title} thành công trên Google Cloud Bucket.")


def sync_to_cloud(cloud_service, lesson):
    if not hasattr(cloud_service, "upload_lesson") or not callable(getattr(cloud_service, "upload_lesson")):
        raise AttributeError("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông")
    cloud_service.upload_lesson(lesson)


def main():
    lessons = []
    current_lesson = None

    def case_recruitment():
        nonlocal current_lesson
        print("\n--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
        print("1. Video Lesson (Bài học Video Lý Thuyết)")
        print("2. Coding Challenge (Bài tập Thực Hành Code)")
        print("3. Hybrid Assessment (Bài Kiểm Tra Tổng Hợp)")
        type_choice = input("Chọn loại bài học (1-3): ")
        
        lesson_code = input("Nhập mã bài học 10 ký tự: ")
        if not BaseLesson.validate_lesson_code(lesson_code):
            print("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
            return

        title = input("Nhập tiêu đề bài học: ")
        
        match type_choice:
            case "1":
                lesson = VideoLesson(lesson_code, title)
                print(f"Khởi tạo bài học Video thành công!\nTiêu đề bài học: {lesson.title}")
            case "2":
                lesson = CodingChallenge(lesson_code, title)
                print(f"Khởi tạo bài tập Thực Hành Code thành công!\nTiêu đề bài học: {lesson.title}")
            case "3":
                lesson = HybridAssessment(lesson_code, title)
                lesson.set_duration(45)  
                print(f"Khởi tạo bài học Hybrid thành công!\nTiêu đề bài học: {lesson.title}")
            case _:
                print("Lựa chọn loại nội dung không hợp lệ.")
                return

        lessons.append(lesson)
        current_lesson = lesson

    def case_view_info():
        if not current_lesson:
            print("Chưa có bài học nào được chọn hoặc khởi tạo trong hệ thống!")
            return
        print("\n--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
        print(f"Loại bài học: {type(current_lesson).__name__}")
        print(f"Nền tảng: {current_lesson.platform_name}")
        print(f"Mã bài học: {current_lesson.lesson_code}")
        print(f"Tiêu đề bài học: {current_lesson.title}")
        print(f"Thời lượng bài học: {current_lesson.duration_minutes} phút")
        
        if isinstance(current_lesson, VideoLesson):
            print(f"Chất lượng video: {current_lesson.video_quality}")
            print(f"Số lượt xem: {current_lesson.view_count} lượt")
        if isinstance(current_lesson, CodingChallenge):
            print(f"Số lượng testcase lập trình: {current_lesson.number_of_testcases} bài")
            print(f"Hệ số độ khó: {current_lesson.difficulty_multiplier}")
            
        print(f"Thứ tự kế thừa (MRO): {[cls.__name__ for cls in type(current_lesson).__mro__]}")

    def case_update_content():
        if not current_lesson:
            print("Chưa có bài học nào được chọn hoặc khởi tạo trong hệ thống!")
            return
        print("\n--- CẬP NHẬT NỘI DUNG & THỜI LƯỢNG ---")
        print("1. Giả lập học viên tăng lượt xem video (Chỉ dành cho Video/Hybrid)")
        print("2. Cập nhật thông số bài học (Thời lượng, testcase...)")
        task_choice = input("Chọn tác vụ (1-2): ")

        try:
            match task_choice:
                case "1":
                    if isinstance(current_lesson, VideoLesson):
                        current_lesson.play_video()
                        print("Ghi nhận thành công! Học viên đã xem video bài học.")
                        print(f"Tổng số lượt xem hiện tại: {current_lesson.view_count} lượt.")
                    else:
                        print("Tác vụ thất bại! Bài học này không chứa tài nguyên video lý thuyết.")
                case "2":
                    if isinstance(current_lesson, HybridAssessment) or isinstance(current_lesson, CodingChallenge):
                        new_cases = int(input("Nhập số lượng testcase kiểm thử mới bổ sung: "))
                        current_lesson.update_content(new_cases)
                        print("Cập nhật thông số thành công!")
                        print(f"Số lượng testcase hiện tại trên hệ thống: {current_lesson.number_of_testcases} testcases.")
                    elif isinstance(current_lesson, VideoLesson):
                        new_duration = float(input("Nhập số phút thời lượng bài học mới: "))
                        current_lesson.update_content(new_duration)
                        print("Cập nhật thông số thành công!")
                        print(f"Thời lượng bài học hiện tại: {current_lesson.duration_minutes} phút.")
                case _:
                    print("Tác vụ không hợp lệ.")
        except ValueError as e:
            print(f"Lỗi hệ thống khi cập nhật thông số: {e}")

    def case_calculate_score():
        if not current_lesson:
            print("Chưa có bài học nào được chọn hoặc khởi tạo trong hệ thống!")
            return
        total_xp = current_lesson.calculate_completion_score()
        print("\n--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH ---")
        print(f"Bài học: {current_lesson.title} (Loại: {type(current_lesson).__name__})")
        print(f"Điểm cơ sở hệ thống: {current_lesson.base_completion_points} XP")
        print(f"Thời lượng tích lũy: {current_lesson.duration_minutes} phút")
        if isinstance(current_lesson, CodingChallenge):
            print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")
        print(f"Tổng điểm kinh nghiệm (XP) nhận được khi hoàn thành: {total_xp} XP")

    def case_operator_overloading():
        if not current_lesson:
            print("Chưa có bài học nào được chọn hoặc khởi tạo trong hệ thống!")
            return
        if len(lessons) < 2:
            print("Hệ thống yêu cầu tối thiểu 2 bài học để thực hiện Overloading!")
            return

        print("\nDanh sách bài học hiện tại:")
        for idx, les in enumerate(lessons):
            print(f"{idx}. {les.lesson_code} - {les.title} ({les.duration_minutes} phút)")

        try:
            target_idx = int(input("Chọn số thứ tự bài học đối ứng (B): "))
            if target_idx < 0 or target_idx >= len(lessons):
                print("Lựa chọn nằm ngoài phạm vi danh sách.")
                return

            lesson_b = lessons[target_idx]
            print("\n--- ĐỒNG BỘ & SO SÁNH THỜI LƯỢNG (OPERATOR OVERLOADING) ---")
            print(f"Bài học hiện tại (A): {current_lesson.title} (Thời lượng: {current_lesson.duration_minutes} phút)")
            print(f"Bài học đối ứng (B): {lesson_b.title} (Thời lượng: {lesson_b.duration_minutes} phút)")

            is_less = current_lesson < lesson_b
            comp_result = "NGẮN HƠN" if is_less else "KHÔNG NGẮN HƠN"
            print(f"[Kết quả So sánh (__lt__)]: Thời lượng bài học A {comp_result} thời lượng bài học B.")

            total_duration = current_lesson + lesson_b
            print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng học tập của cả 2 bài học là: {total_duration} phút.")
        except Exception as e:
            print(f"Lỗi tính toán Overloading: {e}")

    def case_duck_typing():
        if not current_lesson:
            print("Chưa có bài học nào được chọn hoặc khởi tạo trong hệ thống!")
            return
        print("\n--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
        print("1. Đồng bộ lên máy chủ AWS S3 Storage")
        print("2. Đồng bộ lên máy chủ Google Cloud Storage")
        print("3. Kích hoạt dịch vụ giả mạo (Kiểm tra bẫy cấu trúc lỗi)")
        cloud_choice = input("Chọn dịch vụ lưu trữ (1-2): ")

        try:
            match cloud_choice:
                case "1":
                    service = AWSS3StorageService()
                    sync_to_cloud(service, current_lesson)
                case "2":
                    service = GoogleCloudStorageService()
                    sync_to_cloud(service, current_lesson)
                case "3":
                    class FakeUnlinkedCloudService: pass
                    service = FakeUnlinkedCloudService()
                    sync_to_cloud(service, current_lesson)
                case _:
                    print("Lựa chọn dịch vụ không hợp lệ.")
        except AttributeError as e:
            print(f"[Bẫy dữ liệu thành công] AttributeError: {e}")

    while True:
        print("\n===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
        print("1. Khởi tạo bài học mới (Chọn loại bài học nội dung)")
        print("2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)")
        print("3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)")
        print("4. Xem chi tiết điểm thưởng hoàn thành bài học")
        print("5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)")
        print("6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)")
        print("7. Thoát chương trình")
        print("==============================================")
        
        choice = input("Chọn chức năng (1-7): ")
        
        match choice:
            case "1": case_recruitment()
            case "2": case_view_info()
            case "3": case_update_content()
            case "4": case_calculate_score()
            case "5": case_operator_overloading()
            case "6": case_duck_typing()
            case "7":
                print("Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!")
                break
            case _:
                print("Chức năng không hợp lệ, vui lòng nhập lại từ 1 đến 7.")


if __name__ == "__main__":
    try:
        print("--- Thử nghiệm bẫy 1 (Khởi tạo lớp trừu tượng trực tiếp) ---")
        abstract_test = BaseLesson("LMS0000000", "Abstract Test")
    except TypeError as e:
        print(f"Hệ thống bảo vệ thành công! Ngăn chặn tạo đối tượng BaseLesson: {e}\n")
        
    main()