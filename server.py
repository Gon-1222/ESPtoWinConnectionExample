import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# TCPサーバーの設定
host = '0.0.0.0'  # ローカルホスト、全てのインターフェースで待機
port = 1234       # ESPの送信先と同じポート番号

# データ受信用のキュー
data_queue = deque(maxlen=100)  # 表示する最大データ数（100サンプル保持）

# グラフの設定
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

ax.set_xlim(0, 100)
ax.set_ylim(0, 4095)  # ESPのアナログ値の範囲（0〜1024）
ax.set_xlabel('Sample')
ax.set_ylabel('Analog Value')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    ydata = list(data_queue)
    xdata = list(range(len(ydata)))
    line.set_data(xdata, ydata)
    return line,

# ソケットの設定とサーバー開始
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()  # ESP32からの接続を待つ
    print(f"Connected by {addr}")

    try:
        while True:
            data = conn.recv(1024)  # 1024バイトまでのデータを受信
            if not data:
                break
            try:
                # 受信データをデコードしてアナログ値に変換
                analog_value = int(data.decode('utf-8').strip())
                print(f"Received value: {analog_value}")
                
                # キューにデータを追加
                data_queue.append(analog_value)
                
            except ValueError:
                # データが整数に変換できなかった場合
                print(f"Error parsing data: {data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()

# アニメーションを開始
ani = animation.FuncAnimation(fig, update, frames=None, init_func=init, interval=100, blit=True)

# サーバーを別スレッドで開始する関数
import threading
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # メインプログラム終了時にスレッドを自動終了
server_thread.start()

# グラフを表示
plt.show()