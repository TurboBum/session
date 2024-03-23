import os
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

def qrcode_new(text, id):
    img = qrcode.make(text)
    filename = f'{text}_{id}.png'
    filepath = os.path.join(os.getcwd(), "qr-cods\\",filename)
    img.save(filepath)
    return filename

def read_qrcode(image_path):
    qr_image = Image.open(image_path)
    qr_code = decode(qr_image)
    if qr_code:
        qr_text = qr_code[0].data.decode("utf-8")
        return qr_text
    else:
        return None

