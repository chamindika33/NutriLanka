import io
import random
from re import sub
import string
import qrcode
import base64
from PIL import Image
import secrets

def get_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img: Image = qr.make_image(fill_color="black", back_color="white")
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format="PNG")
    img_64 = base64.b64encode(imgByteArr.getvalue())
    return ("data:image/png;base64,"+str(img_64.decode("utf-8")))

def get_an_code(k=6):
    alphanum = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=k))
    yield alphanum

def get_digit_code(k=4):
    digit = ''.join(random.choices(string.digits, k=k))
    yield digit

def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    yield''.join([s[0].lower(), s[1:]])

def public_token() -> str:
    secret = secrets.token_hex(4)
    return secret