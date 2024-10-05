import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

# TCPサーバーの設定
host = '0.0.0.0'  # ローカルホスト、全てのインターフェースで待機
port = 1234       # ESPの送信先と同じポート番号

# データ受信用のキュー
data_queue = deque(maxlen=10)  # 表示する最大データ数（100サンプル保持）

# グラフの設定
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

ax.set_xlim(0, 10)
ax.set_ylim(0, 4096)  # ESPのアナログ値の範囲（0〜1024）
ax.set_xlabel('Sample')
ax.set_ylabel('Analog Value')

# 初期化
def init():
    line.set_data([], [])
    return line,

# ソケットの設定とサーバー開始
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()  # ESP32からの接続を待つ
    print(f"Connected by {addr}")
    
    # バッファの蓄積を防ぐために小さいチャンクでデータを受信
    buffer = ""
    try:
        while True:
            # ソケットから1バイトずつ受信
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            
            # 改行区切りでデータを分割
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    analog_value = int(line.strip())
                    print(f"Received value: {analog_value}")
                    
                    # キューにデータを追加
                    data_queue.append(analog_value)
                    
                except ValueError:
                    print(f"Error parsing data: {line}")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()

# データ更新処理（アニメーション）
def update(frame):
    ydata = list(data_queue)
    xdata = list(range(len(ydata)))
    line.set_data(xdata, ydata)
    return line,

# サーバーを別スレッドで開始する関数
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # メインプログラム終了時にスレッドを自動終了
server_thread.start()

# アニメーションを設定（インターバルを100msに調整）
ani = animation.FuncAnimation(fig, update, frames=None, init_func=init, interval=50, blit=True)

# グラフを表示
plt.show()
