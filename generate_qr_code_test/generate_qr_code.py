# Importing library
import qrcode
 
# Data to encode
data = "https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/"
 
# Creating an instance of QRCode class
qr = qrcode.QRCode(version = 1,
                   error_correction = qrcode.constants.ERROR_CORRECT_L,
                   box_size = 20,
                   border = 2)
 
# Adding data to the instance 'qr'
qr.add_data(data)
 
qr.make(fit = True)
img = qr.make_image(fill_color = 'black',
                    back_color = 'white')
 
img.save('MyQRCode2.png')