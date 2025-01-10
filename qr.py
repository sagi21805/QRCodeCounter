import qrcode

# Data to encode
def generate(data: str):
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code, 1 is the smallest
        error_correction=qrcode.ERROR_CORRECT_L,  # Error correction level
        box_size=50,  # Size of each box in pixels
        border=4,  # Border size (minimum is 4)
    )

    # Add data to QR code
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")
