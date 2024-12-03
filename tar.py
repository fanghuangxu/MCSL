import os
import requests
import threading
import time

class DownloadProgress:
    def __init__(self, total_size):
        self.total_size = total_size
        self.downloaded_size = 0

    def update(self, chunk_size):
        self.downloaded_size += chunk_size
        self.print_progress()

    def print_progress(self):
        percentage = (self.downloaded_size / self.total_size) * 100
        speed = self.downloaded_size / (time.time() - start_time) / 1024  # KB/s
        estimated_time = (self.total_size - self.downloaded_size) / speed if speed > 0 else 0
        print(f'\r下载进度: {percentage:.2f}% | 下载速度: {speed:.2f} KB/s | 剩余时间: {estimated_time:.2f} s', end='')

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    progress = DownloadProgress(total_size)

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive chunks
                file.write(chunk)
                progress.update(len(chunk))

if __name__ == "__main__":
    url = "https://download.oracle.com/java/21/archive/jdk-21.0.4_macos-x64_bin.tar.gz"
    save_path = os.path.join(os.getcwd(), "jdk-21.0.4_macos-x64_bin.tar.gz")

    # Start download in a separate thread
    start_time = time.time()
    download_thread = threading.Thread(target=download_file, args=(url, save_path))
    download_thread.start()
    download_thread.join()  # Wait for the thread to finish

    print("\n下载完成!")
