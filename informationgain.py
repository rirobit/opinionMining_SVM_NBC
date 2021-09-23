"""" Entropy(s)
    1.1. entropy (S) (i1 = mengandung fitur a, i2 = tidak mengandung fitur a)
    2.1. entropy (S,a)
    2.2. entropy Spositif (i1 = mengandung fitur a, i2 = tidak mengandung fitur a)
    2.3. entropy Snegatif (i1 = mengandung fitur a, i2 = tidak mengandung fitur a)
    2.4. Spositif yang mengandung fitur a / seluruh s * 2.2.
    2.5. Snegatif yang mengandung fitur a / seluruh s * 2.3.
    2.6. entropy (s,a) = 2.4. + 2.5.
    3.1. Gain(a) = 1.1. - 2.6.
    """

from math import log2


class IGFiturSelection:
    def __init__(self, trainingset, standar):
        self.dataseleksi = trainingset
        self.standarseleksi = standar
        self.fiturunik = []
        self.positif = []
        self.negatif = []
        self.semuadokumen = len(trainingset)

        for i in range(0, self.semuadokumen):
            if self.dataseleksi['opini_label'][i] == 'p':
                self.positif.append(self.dataseleksi['opini_dokumen'][i])
            else:
                self.negatif.append(self.dataseleksi['opini_dokumen'][i])
        self.lpositif = len(self.positif)
        self.lnegatif = len(self.negatif)

    def getfiturunik(self):
        return self.fiturunik

    def proporsi(self, a, b):  # mencari proporsi
        prop = a/b
        return prop

    def entropy(self, a, b):  # mencari entropy
        def logaritma(c):
            if c != 0:
                d = c*log2(c)
            else:
                d = 0
            return d

        ent = -(logaritma(a)+logaritma(b))

        return ent

    def fitur(self, opini):
        fitur = []
        for dokumen in opini:
            for unik in dokumen:
                if unik in fitur:
                    continue
                else:
                    if unik == '':
                        continue
                    else:
                        fitur.append(unik)
        self.fiturunik = fitur.copy()
        return fitur

    def hitunggain(self, fitur):
        fiturinpositif = 0
        fiturinnegatif = 0
       # p = []

        for dok in self.positif:
            if fitur in dok:
                fiturinpositif += 1
        for dok in self.negatif:
            if fitur in dok:
                fiturinnegatif += 1
        existall = fiturinpositif + fiturinnegatif
        proporsiada = self.proporsi(existall, self.semuadokumen)
        proporsitidakada = self.proporsi(self.semuadokumen - existall, self.semuadokumen)
        entropys = self.entropy(proporsiada, proporsitidakada)
        proposiapos = self.proporsi(fiturinpositif, self.semuadokumen)
        proposinonapos = self.proporsi(self.lpositif-fiturinpositif, self.lpositif)
        proposianeg = self.proporsi(fiturinnegatif, self.lnegatif)
        proposinonaneg = self.proporsi(self.lnegatif-fiturinnegatif, self.lnegatif)
        entropyapos = self.entropy(proposiapos, proposinonapos)
        entropyaneg = self.entropy(proposianeg, proposinonaneg)
        paposdok = self.proporsi(fiturinpositif, self.semuadokumen)
        panegdok = self.proporsi(fiturinnegatif, self.semuadokumen)
        entropysa = paposdok * entropyapos + panegdok * entropyaneg
        gainsa = entropys - entropysa
        return gainsa

    def seleksifitur(self):
        standar = self.standarseleksi
        dokumen = self.dataseleksi
        opini = dokumen['opini_dokumen']
        fitur = self.fitur(opini)
        for kata in fitur:
            gainkata = self.hitunggain(kata)
            if gainkata < standar:
                self.fiturunik.remove(kata)
        return self.fiturunik