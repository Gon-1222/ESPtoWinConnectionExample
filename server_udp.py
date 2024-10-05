import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

# UDPサーバーの設定
host = '0.0.0.0'  # ローカルホスト、全てのインターフェースで待機
port = 1234       # ESPの送信先と同じポート番号

# データ受信用のキュー
data_queue = deque(maxlen=100)  # 表示する最大データ数（100サンプル保持）

# グラフの設定
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

ax.set_xlim(0, 100)
ax.set_ylim(0, 4096)  # ESPのアナログ値の範囲（0〜1024）
ax.set_xlabel('Sample')
ax.set_ylabel('Analog Value')

# 初期化
def init():
    line.set_data([], [])
    return line,

# ソケットの設定とサーバー開始
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server listening on {host}:{port}")

    # UDPでデータを受信
    while True:
        try:
            # データ受信
            data, addr = server_socket.recvfrom(1024)  # 1024バイトまでのデータを受信
            data = data.decode('utf-8').strip()
            print(f"Received data: {data} from {addr}")
            
            try:
                analog_value = int(data)
                
                # キューにデータを追加
                data_queue.append(analog_value)
                
            except ValueError:
                print(f"Error parsing data: {data}")
        
        except Exception as e:
            print(f"Error: {e}")
            break

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

# アニメーションを設定（インターバルを50msに調整）
ani = animation.FuncAnimation(fig, update, frames=None, init_func=init, interval=50, blit=True)

# グラフを表示
plt.show()
