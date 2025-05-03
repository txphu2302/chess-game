# ♟️ Trò Chơi Cờ Vua

Một trò chơi cờ vua đơn giản được lập trình bằng Python và Pygame, có giao diện đồ họa và đối thủ AI với các mức độ khó tùy chỉnh.

---

## 📝 Mô Tả

Dự án này là một trò chơi cờ vua 2D, cho phép người chơi đấu với AI hoặc xem hai AI thi đấu trong chế độ demo. Các tính năng bao gồm:

- **Chế độ Người vs AI**: Chơi với vai trò Trắng hoặc Đen chống lại AI với ba mức độ khó (Dễ, Trung Bình, Khó).
- **Chế độ AI vs AI (Demo)**: Xem AI Trắng (dùng mức độ khó đã chọn) thi đấu với AI Đen (dùng logic ngẫu nhiên như mức Dễ).
- **Các tính năng nổi bật**:
  - Kiểm tra nước đi hợp lệ
  - Phát hiện chiếu, chiếu hết, và bế tắc
  - Chọn phong cấp
  - Hiệu ứng âm thanh
  - AI đơn giản dựa trên thuật toán minimax với cắt tỉa alpha-beta

---

## ⚙️ Cài Đặt

### Yêu Cầu

- Python 3.x  
- Thư viện:
  - `pygame`
  - `python-chess`

### Thiết Lập

```bash
# Clone repository
git clone https://github.com/txphu2302/chess-game
cd chess-game

# Cài đặt các thư viện
pip install -r requirements.txt

```

## 📁 Thư Mục **assets** Cần Chứa

**File âm thanh:**
- move-self.wav
- capture.wav
- castle.wav
- move-check.wav


**Hình ảnh quân cờ:**
- Quân trắng
    - wP.png, wN.png, wB.png, wR.png, wQ.png, wK.png
- Quân đen
    - bP.png, bN.png, bB.png, bR.png, bQ.png, bK.png

⚠️ Lưu ý: Nếu thiếu tài nguyên, trò chơi sẽ sử dụng ký tự văn bản thay thế.

## ▶️ Chạy Trò Chơi

```bash
python chess_game.py

```

## 🎮 Hướng Dẫn Sử Dụng

### Menu Chính

- **Người vs AI**: Chọn màu (Trắng, Đen, Ngẫu nhiên) và mức độ khó (Dễ, Trung Bình, Khó, hoặc Ngẫu nhiên).

- **AI vs AI (Demo)**: Xem hai AI tự động thi đấu.

- **Thoát Trò Chơi**: Thoát khỏi ứng dụng.

### Trong Trò Chơi

- **Di chuyển quân**: Nhấp vào quân → nhấp vào ô muốn đi nếu hợp lệ.

- **Phong cấp**: Chọn quân (Hậu, Xe, Tượng, Mã) khi Tốt đến cuối bàn.

- **Kết thúc**: Hiển thị trạng thái chiếu hết, bế tắc hoặc hòa, kèm tùy chọn chơi lại hoặc quay về menu.

- **Thanh thông tin**: Hiển thị lượt đi, độ khó, và các nút điều hướng.

### Điều Khiển

- **Chuột**: Dùng để chọn và di chuyển quân.

- **Nút giao diện**: Thao tác trong menu và khi kết thúc ván.

## 🧠 Tính Năng
### Mức Độ Khó
- **Dễ**: AI đi ngẫu nhiên, ưu tiên bắt quân (70%).

- **Trung Bình**: Sử dụng thuật toán Minimax độ sâu 1.

- **Khó**: Minimax có cắt tỉa alpha-beta, độ sâu 3 (chậm hơn nhưng thông minh hơn).

### AI vs AI (Demo)
- AI Trắng dùng độ khó do người dùng chọn.

- AI Đen sử dụng chiến thuật ngẫu nhiên như mức Dễ.

### Hiệu Ứng
- **Hoạt ảnh**: Tô màu ô được chọn, nước đi cuối cùng, cảnh báo chiếu.

- **Âm thanh**: Kêu hiệu ứng khi di chuyển, ăn quân, nhập thành, chiếu nếu có file tương ứng.

## 🛠️ Phát Triển
### Đóng Góp
Bạn có thể fork repository và gửi Pull Request.
Đóng góp được hoan nghênh, đặc biệt là:

- Cải tiến thuật toán AI

- Giao diện người dùng đẹp hơn

- Thêm chức năng như lưu/load ván cờ

## ⚠️ Vấn Đề Đã Biết
- Các hiệu ứng âm thanh yêu cầu đúng file tên trong thư mục assets.

- Ở độ khó cao, AI có thể tính toán hơi lâu tùy vào máy tính của bạn.

## 📄 Giấy Phép
Phần mềm này sử dụng Giấy phép MIT.
Bạn có thể dùng, sửa đổi, phân phối lại miễn phí theo điều kiện trong giấy phép.

## 📬 Liên Hệ
📧 Email: toilaphu23@example.com

🐞 Gửi lỗi / góp ý: Vui lòng mở issue trên GitHub repository
