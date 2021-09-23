import preprocessing
import informationgain


class Trainingset:
    def __init__(self, dataset, standar):
        self.training = dataset
        self.probabilitasfitur = {}  # dictionary kata pada label positif dan negatif dengan key : kata tersebut
        self.probabilitaslabel = {'positif': 0.0, 'negatif': 0.0}
        trainingopini = self.training['opini_dokumen']
        prepo = preprocessing.Preprocessing
        trainingopini = prepo.cleaning(trainingopini)
        trainingopini = prepo.normalization(trainingopini)
        trainingopini = prepo.stemming(trainingopini)
        trainingopini = prepo.stopwordremoval(trainingopini)
        trainingopini = prepo.convertnegation(trainingopini)
        trainingopini = prepo.tokenization(trainingopini)
        self.training['opini_dokumen'] = trainingopini
        ig = informationgain.IGFiturSelection(self.training, standar)
        fitur = ig.seleksifitur()
        self.trainy(fitur)

    def get_training(self):
        return self.training

    def get_opini(self):
        return self.training['opini_dokumen']

    def get_prob(self):
        return self.probabilitasfitur

    def get_label(self):
        return self.probabilitaslabel

    def trainy(self, unik):
        dok = self.training
        p = 0  # jumlah dokumen positif
        n = 0  # jumlah dokumen negatif
        wordp = []  # list kata dalam dokumen positif
        wordn = []  # list kata dalam dokumen negatif
        banyak = len(dok)  # jumlah dokumen training

        for i in range(0, banyak):
            if dok['opini_label'][i] == 'p':
                p += 1
                for w in dok['opini_dokumen'][i]:
                    wordp.append(w)
            else:
                n += 1
                for w in dok['opini_dokumen'][i]:
                    wordn.append(w)

        word = 0  # jumlah kata dalam seluruh dokumen training

        for d in dok['opini_dokumen']:
            word += len(d)

        self.probabilitaslabel['positif'] = p/banyak  # probabilitas label positif
        self.probabilitaslabel['negatif'] = n/banyak  # probabilitas label negatif

        for d in dok['opini_dokumen']:
            nn = 0
            np = 0
            for w in d:
                if w in unik:
                    if w in self.probabilitasfitur:
                        continue
                    else:
                        prob = []
                        for wt in wordp:
                            if wt == w:
                                np += 1

                        for wt in wordn:
                            if wt == w:
                                nn += 1
                    papos = (np + 1)/(p + len(unik))
                    paneg = (nn + 1)/(n + len(unik))
                    prob.append(papos)
                    prob.append(paneg)
                    self.probabilitasfitur[w] = prob