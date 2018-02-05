# -*- coding: utf-8 -*-
import nfc
import binascii

#カードを読み取り
def connected(tag):
    global idm
    idm = binascii.hexlify(tag.idm)

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected}) # now touch a tag
clf.close()

#IDmを表示
print idm
