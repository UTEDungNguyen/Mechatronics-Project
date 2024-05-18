
from barcode.ean import EAN13
from barcode.writer import ImageWriter
from random import randint

from openpyxl import  Workbook
from openpyxl.drawing.image import Image
import cv2
from pyzbar import pyzbar

# from PIL import Image

# import Image



pd_code =''

for i in range (0,12):
    num = randint(1,9)
    pd_code = pd_code + str(num)
    # Replace with your actual data
# print(pd_code)
ean = EAN13(pd_code, writer=ImageWriter())
filename = ean.save('ean13_barcode')

img= Image(filename)
img.height = 30
img.width = 100



wbook = Workbook()
wsheet = wbook.active

wsheet.title ="Test_Datasheet"
# wbook.save('T_dt.xlsx')

### CREATE TITLE FOR CELL ###
wsheet['A1'] = 'STT'
wsheet['B1'] = 'Mass'
wsheet['C1'] = 'Production'
wsheet['D1'] = 'Barcode_Image'

###############################
wsheet['A2'] = '1'
wsheet['B2'] = '2500'
wsheet['C2'] = pd_code
wsheet.add_image(img, 'D2')


wbook.save('T_dt.xlsx')

######################################## SCAN BARCODE ##########################################


