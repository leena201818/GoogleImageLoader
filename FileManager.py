# encoding=utf-8
import random,os
from PIL import Image


'''
Delete non-jpg files
'''
def DeleteNoJPGFile(dir):
    w = os.walk(dir)
    for path,subpath,files in w:
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext.lower() != '.jpg':
                fullpath = os.path.join(path,file)
                os.remove(fullpath)
                print('delete {0}'.format(fullpath))

'''
Rename file name with prefix and 6 bit number 
'''
def RenameFileName(dir,prefix='logo_'):
    w = os.walk(dir)
    num = 1
    for path, subpath, files in w:
        for file in files:
            ext = os.path.splitext(file)[1]
            newfileename = "{0}{1}.jpg".format(prefix,'%06d'%(num))
            num=num+1
            if ext.lower() == '.jpg':
                fullpath = os.path.join(path, file)
                newpath = os.path.join(path,newfileename )
                print(fullpath,newpath)
                os.rename(fullpath,newpath)
                print('rename {0} to {1}'.format(fullpath,newfileename))
'''
Rename directiory name with frefix and 2 bit number
'''
def RenameDir(dir,prefix='sam_'):
    w = os.walk(dir)
    num = 0
    for path, subpath, files in w:
        for sp in subpath:
            newpath = "{0}{1}".format(prefix,'%02d'%(num))
            num=num+1
            print(subpath,newpath)
            os.rename(os.path.join(path,sp),os.path.join(path,newpath))
            print('rename {0} to {1}'.format(subpath,newpath))

'''
Delete the duplicate file, using the file hash method
'''
import hashlib,shutil
def DeleteDuplx(dir):
    backdir = os.path.join(r'D:\img\samples\duplicate')
    if not os.path.exists(backdir):
        os.makedirs(backdir)

    h = hashlib.md5
    picSet = {}

    w = os.walk(dir)
    num = 1
    for path, subpath, files in w:
        for file in files:
            ext = os.path.splitext(file)[1]
            num = num + 1
            if ext.lower() == '.jpg':
                fullpath = os.path.join(path, file)

                picMd5 = ''
                with open(fullpath, 'rb') as pic:
                    picMd5 = hashlib.md5(pic.read()).hexdigest()

                if picMd5 in picSet:
                    shutil.move(fullpath,os.path.join(backdir,file))
                    print('move {0} to {1}!'.format(fullpath,backdir))
                else:
                    picSet[picMd5]=fullpath
                    # print('put {0} to dictionary,and the MD5 is : {1}'.format(fullpath,picMd5))
'''
Resize image size and save as file with prefix and 6 bit number
'''
def Resize(dir,targetdir,width,height,prefix='sam_'):
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)

    num = 0
    w = os.walk(dir)
    for path, subpath, files in w:
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext.lower() == '.jpg':
                fullpath = os.path.join(path, file)
                img = Image.open(fullpath)
                out =img.resize((width,height),Image.ANTIALIAS)
                newfilename = "{0}{1}.jpg".format(prefix,'%06d'%(num))
                num = num+1
                resizedir =os.path.join(targetdir,newfilename)
                out.save(resizedir)

                print('resize {0} to {1}'.format(file,resizedir))

# copy all file to targetdir
def CopyFile(sourdir,targetdir,prefix='m_'):
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    num = 0
    w = os.walk(sourdir)
    for path,subpath,files in w:
        for file in files:
            fullpath = os.path.join(path,file)
            newfilename = '{}{}.jpg'.format(prefix,'%06d'%(num))
            tarfullpath = os.path.join(targetdir, newfilename)
            num+=1
            shutil.copy(fullpath, tarfullpath)
            print('move {0} to {1}!'.format(fullpath, tarfullpath))
# copy source file with regurl experssion to target
import re
def CopyFile3(sourdir,targetdir,sourRE = r'\\sam_\d\d',prefix='m_'):
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    num = 0
    w = os.walk(sourdir)

    for path,subpath,files in w:
        print(path)
        if re.match(sourRE,path) is  not None:# and re.match('.*sam_\d{2}_\d',path) is None:
            print(path)
            # for file in files:
            #     fullpath = os.path.join(path,file)
            #     newfilename = '{}{}.jpg'.format(prefix,'%06d'%(num))
            #     tarfullpath = os.path.join(targetdir, newfilename)
            #     num+=1
            #     shutil.copy(fullpath, tarfullpath)
            #     print('move {0} to {1}!'.format(fullpath, tarfullpath))

#copy source dir with postfix to targetdir
def CopyFile(sourdir,postfix,targetdir,prefix='m_'):
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    num = 0
    w = os.walk(sourdir)
    for path,subpath,files in w:
        print(path)
        if path.endswith(postfix):

            for file in files:
                fullpath = os.path.join(path,file)
                newfilename = '{}{}.jpg'.format(prefix,'%06d'%(num))
                tarfullpath = os.path.join(targetdir, newfilename)
                num+=1
                shutil.copy(fullpath, tarfullpath)
                print('move {0} to {1}!'.format(fullpath, tarfullpath))


if __name__ == '__main__':
    # RenameDir(r'D:\img\samples\resultbyimg')

    dir = r'D:\img\cnnSamples\nor'
    RenameFileName(dir,prefix='nor_')

    # sd = r'D:\img\samples\mil by m\mil sam00-22'
    # td = r'D:\img\samples\mil by m\mil_by_m'
    # CopyFile3(sd,td,sourRE='sam_\d[2][^_]',prefix='m_')

    # dir = r'D:\img\samples\normal'
    # targetdir = r'D:\img\samples\nor_100X100'
    #
    # Resize(dir,targetdir,100,100,prefix='nor_')
    #
    # # DeleteNoJPGFile(path)
    # # RenameFileName(path,'normal_')
    #
    # DeleteDuplx(path)
