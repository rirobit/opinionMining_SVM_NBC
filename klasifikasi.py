import preprocessing
import pandas as pd
import mysql.connector

class Klasifikasi:
    def __init__(self, query, con):
        self.dataset = pd.read_sql_query(query, con)
        prepro = preprocessing.Preprocessing
        opini = self.dataset['opini_dokumen']
        opini = prepro.cleaning(opini)
        opini = prepro.normalization(opini)
        opini = prepro.stemming(opini)
        opini = prepro.stopwordremoval(opini)
        opini = prepro.convertnegation(opini)
        opini = prepro.tokenization(opini)
        self.dataset['opini_dokumen'] = opini
        self.mydb = con

    def getdataset(self):
        return self.dataset

    def getopini(self):
        return self.dataset['opini_dokumen']

    def classifikasi(self, plabel, pfitur):
        curl = self.mydb.cursor()
        jumlah = len(self.dataset)
        sentimen = ''
        for i in range(0, jumlah):
            opini = self.dataset['opini_dokumen'][i]
            index = str(self.dataset['opini_id'][i])
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
            sql = "UPDATE opini SET opini_label = %s WHERE opini_id = %s"
            val = (sentimen, index)
            curl.execute(sql, val)
            self.dataset['opini_label'][i] = sentimen
        self.mydb.commit()