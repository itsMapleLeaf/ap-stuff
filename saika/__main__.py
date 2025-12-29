import webview

window = webview.create_window("d", "http://localhost:5173/")
webview.start(ssl=True)
