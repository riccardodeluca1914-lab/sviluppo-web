from flask import Flask
import random


app = Flask(__name__)

@app.route('/')
def ciao_mondo():
    return '<h1>Benvenut@! Questo è un sito su come la tecnologia fa diventare dipendenti.</h1><br><a href="/fatti_interessanti">Scopri un fatto interessante!</a>'


@app.route('/fatti_interessanti')
def fun_fact():
    lista =['La maggior parte delle persone che soffrono di dipendenza tecnologica sperimentano un forte stress quando si trovano al di fuori dell"area di copertura della rete o non possono utilizzare i loro dispositivi', 'Secondo uno studio condotto nel 2018, più del 50% delle persone di età compresa tra i 18 e i 34 anni si considera dipendente dal proprio smartphone', 'Lo studio della dipendenza tecnologica è una delle aree più rilevanti della ricerca scientifica moderna', 'Secondo uno studio del 2019, oltre il 60% delle persone risponde ai messaggi di lavoro sul proprio smartphone entro 15 minuti dall"uscita dal lavoro.','Un modo per combattere la dipendenza tecnologica è cercare attività che portino piacere e migliorino l"umore','Elon Musk sostiene che i social network sono progettati per tenerci all"interno della piattaforma, in modo che trascorriamo il maggior tempo possibile a guardare contenuti','Elon Musk sostiene che i social network sono progettati per tenerci all"interno della piattaforma, in modo che trascorriamo il maggior tempo possibile a guardare contenuti','I social network hanno aspetti positivi e negativi e dobbiamo essere consapevoli di entrambi quando usiamo queste piattaforme.']
    return f'<h1>{random.choice(lista)}</h1><br><a href="/">Torna alla home</a>'


app.run(debug=True)