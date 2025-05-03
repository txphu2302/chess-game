Trò Chơi Cờ Vua
Một trò chơi cờ vua đơn giản được lập trình bằng Python và Pygame, có giao diện đồ họa và đối thủ AI với các mức độ khó tùy chỉnh.
Mô Tả
Dự án này là một trò chơi cờ vua 2D, cho phép người chơi đấu với AI hoặc xem hai AI thi đấu trong chế độ demo. Các tính năng bao gồm:

Chế độ Người vs AI: Chơi với vai trò Trắng hoặc Đen chống lại AI với ba mức độ khó (Dễ, Trung Bình, Khó).
Chế độ AI vs AI (Demo): Xem AI Trắng (sử dụng mức độ khó đã chọn) thi đấu với AI Đen (sử dụng logic ngẫu nhiên giống mức Dễ).
Tính năng: Kiểm tra nước đi hợp lệ, phát hiện chiếu/các nước chiếu hết, chọn phong cấp, hiệu ứng âm thanh, và AI đơn giản dựa trên thuật toán minimax với cắt tỉa alpha-beta.

Cài Đặt
Điều Kiện Tiền Thiệt

Python 3.x
Thư viện cần thiết:
pygame
python-chess



Thiết Lập

Clone repository:
git clone https://github.com/username/ChessGame.git
cd ChessGame


Cài đặt các thư viện:
pip install pygame python-chess


Đảm bảo thư mục assets chứa:

File âm thanh: move-self.wav, capture.wav, castle.wav, move-check.wav
Hình ảnh quân cờ: wP.png, wN.png, wB.png, wR.png, wQ.png, wK.png, bP.png, bN.png, bB.png, bR.png, bQ.png, bK.png
(Nếu thiếu, trò chơi sẽ sử dụng hình ảnh thay thế bằng văn bản.)


Chạy trò chơi:
python chess_game.py



Hướng Dẫn Sử Dụng
Menu Chính

Người vs AI: Chọn màu cờ (Trắng, Đen, hoặc Ngẫu nhiên) và mức độ khó (Dễ, Trung Bình, Khó, hoặc Ngẫu nhiên).
AI vs AI (Demo): Xem hai AI thi đấu, với AI Trắng dùng mức độ khó đã chọn và AI Đen dùng logic ngẫu nhiên.
Thoát Trò Chơi: Thoát ứng dụng.

Trong Trò Chơi

Nhấp chuột vào quân cờ để chọn, sau đó nhấp vào ô đích hợp lệ để di chuyển.
Phong cấp: Khi quân tốt đến cuối bàn cờ đối phương, chọn một quân (Hậu, Xe, Tượng, Mã) từ menu phong cấp.
Kết Thúc Trò Chơi: Hiển thị khi có chiếu hết, bế tắc, hoặc hòa, với tùy chọn chơi lại hoặc trở về menu chính.
Thanh Thông Tin: Hiển thị lượt đi, mức độ khó, và các nút để bắt đầu lại hoặc quay về menu chính.

Điều Khiển

Chuột: Nhấp để chọn và di chuyển quân cờ.
Nút: Sử dụng các nút trên màn hình để điều hướng menu và hành động trong trò chơi.

Tính Năng

Mức Độ Khó:
Dễ: Nước đi ngẫu nhiên với 70% cơ hội bắt quân.
Trung Bình: Thuật toán minimax cơ bản với độ sâu 1.
Khó: Thuật toán minimax với cắt tỉa alpha-beta và độ sâu 3.


Chế độ AI vs AI Demo: AI Trắng dùng mức độ khó đã chọn, AI Đen dùng logic ngẫu nhiên giống mức Dễ.
Hiệu Ứng Thị Giác: Đánh dấu ô đã chọn, nước đi cuối, và trạng thái chiếu.
Hiệu Ứng Âm Thanh: Âm thanh cho nước đi, bắt quân, nhập thành, và chiếu (nếu có file tài nguyên).

Phát Triển
Đóng Góp
Hãy fork repository này và gửi pull request. Các đề xuất cải tiến (ví dụ: AI tốt hơn, giao diện đẹp hơn) luôn được chào đón!
Nhật Ký Thay Đổi

05/03/2025: Điều chỉnh chế độ AI vs AI Demo - AI Trắng dùng mức Khó, AI Đen dùng logic ngẫu nhiên giống mức Dễ. Cải thiện căn chỉnh menu phong cấp và màn hình kết thúc để hiển thị nước đi cuối.

Vấn Đề Đã Biết

Hiệu ứng âm thanh yêu cầu các file tài nguyên cụ thể; nếu thiếu, trò chơi sẽ chuyển sang chế độ thay thế.
Hiệu suất AI có thể chậm ở mức độ khó cao do độ sâu minimax.

Giấy Phép
[Giấy phép MIT] 

Liên Hệ
Để đặt câu hỏi hoặc nhận hỗ trợ, liên hệ [toilaphu23@example.com] hoặc mở một issue trên repository này.
