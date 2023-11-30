import pyqrcode
import qrtools

def encode(data):
    qr_code = pyqrcode.create("some data")
    # qr.png("/qr_dir/horn.png", scale=6)
    return qr_code

def decode(file):
    qr = qrtools.QR()
    qr.decode(file)
    return qr.data
