import time, codecs
import nltk
import re
import csv
import numpy
import itertools
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

ruta = "C:\Users\CodeLines\Documents\UAM\Proyecto Terminal\Base de Datos"
archTxt = open(ruta + "\Tweets3.txt", 'rb')
arrLineas = []
raiz = SnowballStemmer("spanish")
genVector = CountVectorizer(min_df=1)
caracRelevantes = []
vectorCarac = []
strProc = ''
arrProc = []
etiqueta = []
l = 0

class eliminaUTF:
    def __init__(self, archivo):
        self.archTxt = archivo
        header = archTxt.read(4)
        #Bucar la marca de inicio BOM para UTF-8
        extBOM = 0
        caracEncod = [ ( codecs.BOM_UTF32, 4 ),
                        ( codecs.BOM_UTF16, 2 ),
                        ( codecs.BOM_UTF8, 3 ) ]

        # Eliminar los Bytes BOM
        for cabeza, extension in caracEncod:
            if header.startswith(cabeza):
                extBOM = extension
                break
        archTxt.seek(0)
        archTxt.read(extBOM)
        self.readlines = archTxt.readlines
        self.close = archTxt.close

class stemming:
    def __init__(self,arrLineas,etiqueta,strProc,arrProc):
        self.arrLineas = arrLineas
        self.etiqueta = etiqueta
        self.strProc = strProc
        self.arrProc = arrProc
        for i in arrLineas:
            valor = len(word_tokenize(i))
            arrTokens = word_tokenize(i.decode('utf8'))
            etiqueta.append(arrTokens[-1])
            del arrTokens[-1]
            arrProcesado = []
            strVacio = ""

            for i in arrTokens:
                strTemp1 = re.search(r'(ja)([ja])+',i)
                strTemp2 = re.search(r'(je)([je])+',i)
                strTemp3 = re.search(r'(ji)([ji])+',i)
                strTemp4 = len(i)
                if strTemp1:
                    strVacio = re.sub(r'(ja)([ja])+',"risa",i)
                elif strTemp2:
                    strVacio = re.sub(r'(je)([je])+',"risa",i)
                elif strTemp3:
                    strVacio = re.sub(r'(ji)([ji])+',"risa",i)
                elif strTemp4 <= 2:
                    strVacio = re.sub(r'\w\w?',"",i)
                else:
                    strVacio = re.sub(r'\d',"",i)
                strTemp = re.search(r'\d',i)
                if strTemp:
                    strVacio = re.sub(r'\d',"",i)
                strVacio = raiz.stem(strVacio)
                if strVacio not in stopwords.words('spanish'):
                    arrProcesado.append(strVacio)
                    print arrProcesado
            strProc = ' '.join(arrProcesado)
            arrProc.append(strProc)

class vectorizacion:
    def __init__(self,arrProc,genVector):
        self.arrPorcesado = arrProc
        self.genVector = genVector
        print "Conteo de palabras"
        vecX=genVector.fit_transform(arrProc)

class ponderacion:
    def __init__(self,arrProc):
        self.arrPocesado = arrProc
        print "Pesado - tf-idf"
        matrizPesos = TfidfVectorizer(min_df=1)
        vecY=matrizPesos.fit_transform(arrProc)
        self.toarray = vecY.toarray

class escribirCSV:
    def __init__(self,vectorCarac,vecX,vecY,l):
        self.vectorCarac = vectorCarac
        self.vecX = vecX
        self.vecY = vecY
        self.l = l
        print "Escribiendo matriz en archivo CSV"
        with open('E:\elCSV.csv','wb') as arch:
            iArch = 0
            procEscribir1 = csv.writer(arch, delimiter=",")
            [caso.encode('utf-8') for caso in vectorCarac]
            procEscribir = csv.DictWriter(arch, fieldnames=vectorCarac)
            procEscribir1.writerow(vectorCarac)
            for doc in vecY.toarray():
                print "fila: %d" %(iArch)
                iPalabra = 0
                vecDicionario = {}
                for valorW in doc.tolist():
                    caracteristica = vectorCarac[iPalabra]
                    vecDicionario[vectorCarac[iPalabra]]=valorW
                    iPalabra += 1
                vecDicionario[llaveC]= etiqueta[l]
                procEscribir.writerow(vecDicionario)
                l += 1
                iArch +=1
            arch.close

archTxt = eliminaUTF(archTxt)
print "Leyendo tweets"
arrLineas = archTxt.readlines()
strProc = stemming(arrLineas,etiqueta,strProc,arrProc)
vecX = vectorizacion(arrProc,genVector)
vecY = ponderacion(arrProc)
print "Tama�o de vocabulario: %s" % len(genVector.get_feature_names())
vectorCarac=genVector.get_feature_names()
llaveC = "etiqueta"
vectorCarac.append(llaveC)
cambios = escribirCSV(vectorCarac,vecX,vecY,l)
<<<<<<< HEAD
print "Clasificando"
clasificar(archivocsv)
=======
>>>>>>> parent of cb28c51... Adding object clasificar
