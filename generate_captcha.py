#-*- coding:utf-8 -*-
from captcha.image import ImageCaptcha
from PIL import Image
import numpy as np
import random
import string
import de_zaodian

class generateCaptcha():
    def __init__(self,
                 width = 160,#验证码图片的宽
                 height = 60,#验证码图片的高
                 char_num = 4,#验证码字符个数
                 characters = string.digits + string.ascii_lowercase):#验证码组成，数字+小写字母
#        + string.ascii_uppercase +string.ascii_lowercase
        self.width = width         
        self.height = height
        self.char_num = char_num
        self.characters = characters
        self.classes = len(characters)
        
#    def getBinaryImage(img, b=230):
#        
#        for i in range(img.size[0]):
#            for j in range(img.size[1]):
#                if img.getpixel((i,j)) > b:
#                    img.putpixel((i,j), 255)
#                else:
#                    img.putpixel((i,j), 0)
#        return img

#二值化图片
#img为Image类型 b为阈值
    def gen_captcha(self,batch_size = 50):
        X = np.zeros([batch_size,self.height,self.width,1])
        img = np.zeros((self.height,self.width),dtype=np.uint8)
        Y = np.zeros([batch_size,self.char_num,self.classes])
        image = ImageCaptcha(width = self.width,height = self.height)

        while True:
            for i in range(batch_size):
                captcha_str = ''.join(random.sample(self.characters,self.char_num))
                img = image.generate_image(captcha_str).convert('L')
                
#                下面两个是去噪的
                img = de_zaodian.getBinaryImage(img)
                img = de_zaodian.flood_fill(img)
                
                img = np.array(img.getdata())
                X[i] = np.reshape(img,[self.height,self.width,1])/255.0
                for j,ch in enumerate(captcha_str):
                    Y[i,j,self.characters.find(ch)] = 1
            Y = np.reshape(Y,(batch_size,self.char_num*self.classes))
            yield X,Y

    def decode_captcha(self,y):
        y = np.reshape(y,(len(y),self.char_num,self.classes))
        return ''.join(self.characters[x] for x in np.argmax(y,axis = 2)[0,:])

    def get_parameter(self):
        return self.width,self.height,self.char_num,self.characters,self.classes

    def gen_test_captcha(self):
        image = ImageCaptcha(width = self.width,height = self.height)
        captcha_str = ''.join(random.sample(self.characters,self.char_num))
        img = image.generate_image(captcha_str)
        img.save(captcha_str + '.jpg')
        print(captcha_str)
        
        
        img = img.convert('L')
        img = de_zaodian.getBinaryImage(img)
#        img.show()
        img = de_zaodian.flood_fill(img)
#        img.show()
        img.save(captcha_str + '_quzao' + '.jpg')


        X = np.zeros([1,self.height,self.width,1])
        Y = np.zeros([1,self.char_num,self.classes])
#        img = img.convert('L')
        img = np.array(img.getdata())
        X[0] = np.reshape(img,[self.height,self.width,1])/255.0

        for j,ch in enumerate(captcha_str):
            Y[0,j,self.characters.find(ch)] = 1
        Y = np.reshape(Y,(1,self.char_num*self.classes))
        return X,Y
    
#def gen_test_captcha(self):
#        image = ImageCaptcha(width = self.width,height = self.height)
#        captcha_str = ''.join(random.sample(self.characters,self.char_num))
#        img = image.generate_image(captcha_str)
#        img.save(captcha_str + '.jpg')
#
#        X = np.zeros([1,self.height,self.width,1])
#        Y = np.zeros([1,self.char_num,self.classes])
#        img = img.convert('L')
#        img = np.array(img.getdata())
#        X[0] = np.reshape(img,[self.height,self.width,1])/255.0
#        for j,ch in enumerate(captcha_str):
#            Y[0,j,self.characters.find(ch)] = 1
#        Y = np.reshape(Y,(1,self.char_num*self.classes))
#        return X,Y
        
    
#    def gen_captcha(self,batch_size = 50):
#        X = np.zeros([batch_size,self.height,self.width,1])
#        img = np.zeros((self.height,self.width),dtype=np.uint8)
#        Y = np.zeros([batch_size,self.char_num,self.classes])
#        image = ImageCaptcha(width = self.width,height = self.height)
#
#        while True:
#            for i in range(batch_size):
#                captcha_str = ''.join(random.sample(self.characters,self.char_num))
#                img = image.generate_image(captcha_str).convert('L')
#                img = np.array(img.getdata())
#                X[i] = np.reshape(img,[self.height,self.width,1])/255.0
#                for j,ch in enumerate(captcha_str):
#                    Y[i,j,self.characters.find(ch)] = 1
#            Y = np.reshape(Y,(batch_size,self.char_num*self.classes))
#            yield X,Y
#
#    def decode_captcha(self,y):
#        y = np.reshape(y,(len(y),self.char_num,self.classes))
#        return ''.join(self.characters[x] for x in np.argmax(y,axis = 2)[0,:])
#
#    def get_parameter(self):
#        return self.width,self.height,self.char_num,self.characters,self.classes
