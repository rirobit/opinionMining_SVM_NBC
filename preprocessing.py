from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary


# class untuk mengubah kumpulan dokumen menjadi fitur2 kata dasar
class Preprocessing:
    # cleaning berfungsi untuk menghidangkan simbol tanda baca dalam semua dokumen
    # parameter dok diisi dengan dataset berupa kumpulan kaliman/dokumen
    def cleaning(dok):
        file = dok
        kar = ["\`", "\~", "\!", "\@", "\#", "\$", "\%", "\^", "\&", "\*", "\(", "\)", "\_", "\-", "\+", "\=", "\'", "\;", "\:", "\|", "\\", "\<", "\,", "\>", "\.", "\?", "\/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "\""]
        for char in kar:
            if isinstance(file, str):
                file = str(file).replace(char, "")
            else:
                file = file.astype(str).str.replace(char, "")
        return file

    """normalization berfungsi untuk mengubah kata tidak baku menjadi baku. kata tidak baku bisa terjadi akibat dari salah ketik dan penggunaan bahasa asing. di dalam normalization juga dilakukan proses sase folding yaitu mengubah semua huuf menjadi lower case atau non kapital"""
    def normalization(dok):
        file = dok
        if isinstance(file, str):
            file = file.lower()
            tidak = [' tdk ', ' tak ', ' gak ', ' nggak ', ' nda ', 'no ']
            bapak = [' bpk ', ' bapk ', ' bpak ', ' bapa ', ' pak ', ' pk ']
            cepat = [' cepar ', ' cpt ', ' cpat ', ' cept ', 'cepay']
            file = file.replace(' bu ', ' ibu ')
            file = file.replace(' tp ', ' tapi ')
            file = file.replace('smoking', 'rokok')
            file = file.replace('stop', 'berhenti')
            file = file.replace('love', 'cinta')
            file = file.replace('comment', 'komentar')
            file = file.replace(' nunggu', ' tunggu')
            for w in tidak:
                file = file.replace(w, ' tidak ')
            for w in bapak:
                file = file.replace(w, ' bapak ')
            for w in cepat:
                file = file.replace(w, ' cepat ')
        else:
            file = file.str.lower()
            tidak = [' tdk ', ' tak ', ' gak ', ' nggak ', ' nda ', 'no ']
            bapak = [' bpk ', ' bapk ', ' bpak ', ' bapa ', ' pak ', ' pk ']
            cepat = [' cepar ', ' cpt ', ' cpat ', ' cept ', 'cepay']
            file = file.str.replace(' bu ', ' ibu ')
            file = file.str.replace(' tp ', ' tapi ')
            file = file.str.replace('smoking', 'rokok')
            file = file.str.replace('stop', 'berhenti')
            file = file.str.replace('love', 'cinta')
            file = file.str.replace('comment', 'komentar')
            file = file.str.replace(' nunggu', ' tunggu')
            for w in tidak:
                file = file.str.replace(w, ' tidak ')
            for w in bapak:
                file = file.str.replace(w, ' bapak ')
            for w in cepat:
                file = file.str.replace(w, ' cepat ')
        return file

    """stemming berfungsi untuk mengubah setiap kata menjadi kata dasar dengan menghilangkan imbuhan yang menyertainya. dalam proses ini menggunakan library dari sastrawi."""
    def stemming(dok):
        file = dok
        factory = StemmerFactory()  # membuat objek koleksi kata dasar dari sastrawi
        stemmer = factory.create_stemmer()
        banyak = len(file)
        if isinstance(file, str):
            file = stemmer.stem(file)
        else:
            for i in range(0, banyak):
                bersih = stemmer.stem(file.__getitem__(i))
                file.loc.__setitem__(i, bersih)
        return file

    # menghilangkan stop word atau kata tidak mempengaruhi makna kalimat. proses menggunkan library sastrawi
    def stopwordremoval(dok):
        file = dok
        factory = StopWordRemoverFactory()  # membuat objek untuk menampung koleksi stopword dari sastrawi
        stopword = factory.get_stop_words()
        # menghilangkan kata yang dianggap mempengaruhi sentimen sebuah kalimat dari koleksi stopword agar tidak dihapus dalam proses stopword removal
        stopword.remove('tidak')
        stopword.remove('bukan')
        stopword.remove('belum')
        stopword.remove('kurang')
        stopword.remove('baik')
        stopword.remove('ada')
        dictionary = ArrayDictionary(stopword)
        stopwordremove = StopWordRemover(dictionary)
        banyak = len(file)
        if isinstance(file, str):
            file = stopwordremove.remove(file)
        else:
            for i in range(0, banyak):
                bersih = stopwordremove.remove(file.__getitem__(i))
                file.loc.__setitem__(i, bersih)
        return file

    # frasa dengan awalan negasi digabung menjadi 1 kata
    def convertnegation(dok):
        file = dok
        if isinstance(file, str):
            file = file.replace("tidak ", "tidak")
            file = file.replace("bukan ", "bukan")
            file = file.replace("belum ", "belum")
            file = file.replace("kurang ", "kurang")
        else:
            file = file.str.replace("tidak ", "tidak")
            file = file.str.replace("bukan ", "bukan")
            file = file.str.replace("belum ", "belum")
            file = file.str.replace("kurang ", "kurang")
        return file

    # memisahkan kata per kata dalam sebuah kalimat
    def tokenization(dok):
        file = dok
        if isinstance(file, str):
            file = file.split(" ")
        else:
            file = file.str.split(" ")
        return file