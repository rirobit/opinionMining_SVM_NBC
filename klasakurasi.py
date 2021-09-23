import preprocessing
#import time 

class Klasifikasi:
    def __init__(self, data):
        self.dataset = data
        prepro = preprocessing.Preprocessing
        opini = self.dataset['opini_dokumen']
        opini = prepro.cleaning(opini)
        opini = prepro.normalization(opini)
        opini = prepro.stemming(opini)
        opini = prepro.stopwordremoval(opini)
        opini = prepro.convertnegation(opini)
        opini = prepro.tokenization(opini)
        self.dataset['opini_dokumen'] = opini


    def getdataset(self):
        return self.dataset

    def getopini(self):
        return self.dataset['opini_dokumen']

 

    def classifikasi(self, plabel, pfitur):
        jumlah = len(self.dataset)
        sentimen = ''
        for i in range(0, jumlah):
            opini = self.dataset['opini_dokumen'][i]
            probp = plabel['positif']
            probn = plabel['negatif']
            for w in opini:
                if w in pfitur:
                    probp *= pfitur[w][0]
                    probn *= pfitur[w][1]
                else:
                    continue
            if probp > probn:
                sentimen = 'p'
                
            elif probn > probp:
                sentimen = 'n'
            self.dataset['opini_label'][i] = sentimen
 