import sys, os
import io, math, numpy
from Lod import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

import logging, logging.config

class TextureManager(object):
    '''Texture loading and rendering class'''
   
    def __init__(self, lm):
        logging.config.fileConfig(os.path.join("conf", "log.conf"))
        self.log = logging.getLogger('LOD')
        self.textures = {}
        self.lm = lm

    def GetNewTextureId(self):
        return glGenTextures(1)

    def ReleaseTexture(self, name):
        glDeleteTextures( 1, texture[name]['id'] ) # checks
        pass

    def LoadAtlasTexture(self, tex_name, dirname, imglist, trcol, trimg, status):
        self.log.info("Loading atlas texture \"{}\"".format(tex_name))
        texture_id = self.GetNewTextureId()
        ret = self.lm.GetLod("bitmaps").GetAtlas(imglist, trimg, status)

        img = ret['img']
        width = img.size[0]
        height = img.size[1]
        img = img.convert("RGBA")

        ret2 = self.lm.GetLod("bitmaps").GetFileData("", trimg)
        imgt = 0
        if ret2.get('img_size') is not None:
            imgt = Image.new("P", ret2['img_size'])
            imgt.putdata(ret2['data'])
            imgt.putpalette(ret2['palette'])
            imgt = imgt.convert("RGBA")
            if status == 1:
                imgt = imgt.transpose(Image.FLIP_TOP_BOTTOM)

        if trcol is not None:
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    p = img.getpixel((x, y))
                    if set(p) == set((trcol[0], trcol[1], trcol[2], 255)):
                        img.putpixel((x, y), imgt.getpixel((x%imgt.size[0], y%imgt.size[1])))

        image  = img.tobytes("raw", "RGBA", 0, -1)

        glBindTexture   ( GL_TEXTURE_2D, texture_id )
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri ( GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri ( GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        glTexEnvf (GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        gluBuild2DMipmaps ( GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image )

        # TODO check if name already exists
        self.textures[tex_name] = { 'id': texture_id, 'dir': dirname,
                                    'w': width, 'h': height,
                                    'hstep': ret['hstep'] }
        return True

    def LoadTexture (self, dirname, sfile, trcol=None):
        self.log.info("Loading \"{}/{}\"".format(dirname, sfile))
        ret = self.lm.GetLod(dirname).GetFileData("", sfile) # use try, get rid of ""
        texture_id = self.GetNewTextureId()
        width = 0
        height = 0
        if ret.get('img_size') is not None:
            width  = ret['img_size'][0]
            height = ret['img_size'][1]
            img = Image.new("P", ret['img_size'])
            img.putdata(ret['data'])
            img.putpalette(ret['palette'])
        else:
            fdata = io.BytesIO(ret['data'])
            img = Image.open(fdata)
            width = img.size[0]
            height = img.size[1]

        img = img.convert("RGBA")


        if trcol is not None and trcol != False: # TODO use discard fragment shader
            if trcol == True:
                t = img.getpixel((0, 0))
            else:
                t = trcol
            self.trcol = t

            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    p = img.getpixel((x, y))
                    if set(p) == set((t[0], t[1], t[2], 255)):
                        img.putpixel((x, y), (p[0], p[1], p[2], 0))

        image  = img.tobytes("raw", "RGBA", 0, -1)
        glBindTexture     ( GL_TEXTURE_2D, texture_id )
        glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
        glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
        if trcol != None:
          gl_FragColor = (0xfc,0xfc,0,0xff)
          glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
          glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        else:
          glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
          glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR )
        glTexEnvf (GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        gluBuild2DMipmaps ( GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image )

        self.textures[sfile] = {'id': texture_id, 'dir': dirname,
                               'w': width, 'h': height}
        return True
