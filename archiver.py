#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:53:31 2020

@author: arseniydor
"""

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *

    
import sys
from sys import argv
from struct import *

maximum_table_size = pow(2,int(100))   

def compress(data):
    """Compress a string to a list of output symbols."""
     # Building and initializing the dictionary.
    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.
    
    # iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in data:                     
        string_plus_symbol = string + symbol # get input symbol.
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol
    
    if string in dictionary:
        compressed_data.append(dictionary[string])
    
    output_file = open("encoded.lzw", "wb")
    for data in compressed_data:
        output_file.write(pack('>H',int(data)))
        
    output_file.close()
 


def decompress(file):
    compressed_data = []
    next_code = 256
    decompressed_data = ""
    string = ""
    
    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        compressed_data.append(data)
    
    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
    
    # iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]
    
    # storing the decompressed string into a file.
    output_file = open("decoded.txt", "w")
    for data in decompressed_data:
        output_file.write(data)
        
    output_file.close()


def coding_click(event):
    file = open(libEntry.get(), 'r')
    line = file.read()
    fileReadResult = line
    print(fileReadResult)
    compress(fileReadResult)
    
    
def decoding_click(event):
    file = open(libEntry.get(), 'rb')
    decompress(file)


window = Tk()
window.title("Архиватор")
window.resizable(width=False, height=False) 
window.configure(bg='white')
frame1 = Frame(window, width=300, height=300) 
frame1.grid(row=0, column=0)

btnCod = Button(frame1, width=14, bg='white', font="Verdana 11")
btnCod.place(x=0, y=0)
btnCod['text'] = 'Кодировать'
btnCod.bind('<Button-1>', coding_click)

btnDec = Button(frame1, width=14, bg='white', font="Verdana 11") 
btnDec.place(x=0, y=100)
btnDec['text'] = 'Декодировать'
btnDec.bind('<Button-1>', decoding_click)

libEntry = Entry(frame1, width=18, bd=2, font="Verdana 11") 
libEntry.insert(END, 'archTest.txt')
libEntry.place(x=0, y=200)


window.mainloop()