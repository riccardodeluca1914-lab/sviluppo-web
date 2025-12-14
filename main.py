from flask import Flask, request
import random
import requests

app = Flask(__name__)



TIPI_POKEMON_IT = {
    "normal": "Normale", "fire": "Fuoco", "water": "Acqua", "electric": "Elettro",
    "grass": "Erba", "ice": "Ghiaccio", "fighting": "Lotta", "poison": "Veleno",
    "ground": "Terra", "flying": "Volante", "psychic": "Psico", "bug": "Coleottero",
    "rock": "Roccia", "ghost": "Spettro", "dragon": "Drago", "dark": "Buio",
    "steel": "Acciaio", "fairy": "Folletto"
}

GIOCHI_DEBUTTO_IT = {
    "red-blue": "Rosso & Blu", "yellow": "Giallo", "gold-silver": "Oro & Argento",
    "crystal": "Cristallo", "ruby-sapphire": "Rubino & Zaffiro", "emerald": "Smeraldo",
    "firered-leafgreen": "Rosso Fuoco & Verde Foglia", "diamond-pearl": "Diamante & Perla",
    "platinum": "Platino", "heartgold-soulsilver": "Oro HeartGold & Argento SoulSilver",
    "black-white": "Nero & Bianco", "black-2-white-2": "Nero 2 & Bianco 2",
    "x-y": "X & Y", "omega-ruby-alpha-sapphire": "Rubino Omega & Zaffiro Alpha",
    "sun-moon": "Sole & Luna", "ultra-sun-ultra-moon": "Ultra Sole & Ultra Luna",
    "lets-go-pikachu-lets-go-eevee": "Let's Go, Pikachu! & Let's Go, Eevee!",
    "sword-shield": "Spada & Scudo", "brilliant-diamond-and-shining-pearl": "Diamante Lucente & Perla Splendente",
    "legends-arceus": "Leggende: Arceus", "scarlet-violet": "Scarlatto & Violetto",
    "legends-za": "Leggende: Za", "the-isle-of-armor": "Spada & Scudo DLC 1: L'isola dell'armatura",
    "the-crown-tundra": "Spada & Scudo DLC 2: Le terre della corona",
    "the-teal-mask": "Scarlatto & Violetto DLC 1: La maschera turchese",
    "the-indigo-disk": "Scarlatto & Violetto DLC 2: Il disco indaco"
}



def find_italian_name(names_list):
    """Cerca il nome italiano in una lista 'names' dell'API."""
    for item in names_list:
        if item['language']['name'] == 'it':
            return item['name']
    return None

def extract_evolutions_recursive(chain_link):
    """Estrae ricorsivamente i nomi dalla catena evolutiva."""
    names = []
   
    names.append(chain_link['species']['name'].capitalize())
    
    
    for evolution in chain_link['evolves_to']:
        names.extend(extract_evolutions_recursive(evolution))
    return names

def get_pokemon_full_data():
    """
    Logica completa: Immagine, Tipi, Gen, Giochi, Evoluzioni.
    Restituisce un DIZIONARIO con tutti i dati puliti per l'HTML.
    """
    try:
        random_id = random.randint(1, 1025)
        url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
        
       
        res_pokemon = requests.get(url_pokemon)
        if res_pokemon.status_code != 200: return None
        data_pokemon = res_pokemon.json()
        
        
        img = data_pokemon['sprites']['other']['official-artwork']['front_default']
        if not img: img = data_pokemon['sprites']['front_default']

       
        types_list = [t['type']['name'] for t in data_pokemon['types']]
        types_it = [TIPI_POKEMON_IT.get(t, t.capitalize()) for t in types_list]
        types_str = ", ".join(types_it)

       
        url_species = data_pokemon['species']['url']
        res_species = requests.get(url_species)
        
        name_final = data_pokemon['name'].capitalize()
        generation_str = "Sconosciuta"
        debut_game = "Sconosciuto"
        evo_chain_str = "Nessuna evoluzione"

        if res_species.status_code == 200:
            data_species = res_species.json()
            
            
            it_name = find_italian_name(data_species['names'])
            if it_name: name_final = it_name

            
            url_gen = data_species['generation']['url']
            res_gen = requests.get(url_gen)
            if res_gen.status_code == 200:
                data_gen = res_gen.json()
                gen_it = find_italian_name(data_gen['names'])
                generation_str = gen_it if gen_it else data_species['generation']['name']
                
               
               
                game_list = [vg['name'] for vg in data_gen['version_groups']]
                debut_game = ", ".join([GIOCHI_DEBUTTO_IT.get(g, g.replace('-', ' ').title()) for g in game_list])

            
            url_evo = data_species['evolution_chain']['url']
            res_evo = requests.get(url_evo)
            if res_evo.status_code == 200:
                data_evo = res_evo.json()
                evo_names = extract_evolutions_recursive(data_evo['chain'])
                evo_chain_str = " ➝ ".join(evo_names)

        
        return {
            "name": name_final,
            "image": img,
            "types": types_str,
            "gen": generation_str,
            "games": debut_game,
            "evo": evo_chain_str
        }

    except Exception as e:
        print(f"Errore API: {e}")
        return None


@app.route('/')
def home():
    return """
    <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; color: #333;">
        <h1>Benvenut@ nel Tuo Portale Python!</h1>
        <p>Tutti i tuoi progetti in un unico posto.</p>
        
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; width: 200px; box-shadow: 2px 2px 10px #eee;">
                <h3>🔴 Poké-Dex</h3>
                <p>Scopri dati completi, evoluzioni e generazioni.</p>
                <a href="/pokemon"><button style="padding: 10px; cursor: pointer; background-color: #ff3e3e; color: white; border: none; border-radius: 5px;">Cerca Pokémon</button></a>
            </div>

            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; width: 200px; box-shadow: 2px 2px 10px #eee;">
                <h3>🔒 Sicurezza</h3>
                <form action="/password" method="get">
                    <input type="number" name="lunghezza" min="4" max="20" value="8" style="width: 50px;">
                    <br><br>
                    <button type="submit" style="padding: 10px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">Genera Psw</button>
                </form>
            </div>

            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; width: 200px; box-shadow: 2px 2px 10px #eee;">
                <h3>🪙 Sorte</h3>
                <p>Testa o Croce?</p>
                <a href="/Lanciamoneta"><button style="padding: 10px; cursor: pointer; background-color: #FFC107; border: none; border-radius: 5px;">Lancia</button></a>
            </div>
        </div>
        
        <br><br>
        <a href="/fatti_interessanti">Leggi un fatto interessante</a>
    </div>
    """

@app.route('/pokemon')
def pagina_pokemon():
    
    data = get_pokemon_full_data()
    
    if data:
        
        return f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 40px; min-height: 100vh;">
            
            <div style="background-color: white; border-radius: 20px; padding: 30px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                
                <h5 style="color: #888; text-transform: uppercase; margin: 0;">Pokémon Selvatico</h5>
                <h1 style="font-size: 3em; margin: 10px 0; color: #333;">{data['name']}</h1>
                
                <div style="background-color: #f9f9f9; border-radius: 50%; width: 250px; height: 250px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                    <img src="{data['image']}" width="220" alt="{data['name']}">
                </div>

                <div style="margin-top: 20px; text-align: left;">
                    <p><strong>🧬 Tipi:</strong> {data['types']}</p>
                    <p><strong>📅 Generazione:</strong> {data['gen']}</p>
                    <p><strong>🔗 Catena Evolutiva:</strong><br> 
                       <span style="color: #e91e63; font-weight: bold;">{data['evo']}</span>
                    </p>
                    <p><strong>🎮 Giochi di Debutto:</strong><br> 
                       <span style="font-size: 0.9em; color: #555;">{data['games']}</span>
                    </p>
                </div>
                
                <br>
                <a href="/pokemon"><button style="background-color: #2196F3; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 50px; cursor: pointer; transition: 0.3s;">🔄 Cerca un altro</button></a>
                <br><br>
                <a href="/" style="color: #888; text-decoration: none;">🏠 Torna alla Home</a>
            </div>
        </div>
        """
    else:
        return '<h1>Errore nel caricamento del Pokémon... (Controlla internet o riprova)</h1><a href="/pokemon">Ricarica</a>'



@app.route('/fatti_interessanti')
def fun_fact():
    
    curiosita_tech = [
        "La maggior parte delle persone con dipendenza tecnologica sperimenta forte stress (nomofobia) quando si trova fuori copertura.",
        "Secondo uno studio del 2018, oltre il 50% delle persone tra i 18 e i 34 anni si considera dipendente dal proprio smartphone.",
        "Lo studio della dipendenza tecnologica è oggi una delle aree più rilevanti e attive della ricerca scientifica moderna.",
        "Uno studio del 2019 rivela che oltre il 60% delle persone risponde ai messaggi di lavoro entro 15 minuti dall'uscita dall'ufficio.",
        "Un metodo efficace per combattere la dipendenza è cercare attività 'offline' che portino piacere e migliorino l'umore.",
        "Elon Musk sostiene che i social network sono progettati appositamente per trattenerci sulla piattaforma il più a lungo possibile.",
        "Elon Musk promuove la regolamentazione dei social per proteggere i dati personali ed evitare la manipolazione dei comportamenti.",
        "È fondamentale essere consapevoli che i social network hanno sia aspetti positivi che negativi."
    ]
    
    fact = random.choice(curiosita_tech)
    
    
    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; text-align: center; background-color: #f0f2f5; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 0;">
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 600px;">
            <h2 style="color: #333; margin-top: 0;">💡 Lo sapevi che?</h2>
            <hr style="border: 0; height: 1px; background: #eee; margin: 20px 0;">
            <p style="font-size: 1.3rem; color: #555; line-height: 1.6;">
                {fact}
            </p>
            <br>
            <div style="display: flex; justify-content: center; gap: 10px;">
                <a href="/fatti_interessanti">
                    <button style="background-color: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 50px; cursor: pointer; font-size: 1rem; transition: 0.3s;">
                        🔄 Un'altra!
                    </button>
                </a>
            </div>
            <br>
            <a href="/" style="color: #888; text-decoration: none; font-size: 0.9rem;">🏠 Torna alla Home</a>
        </div>
    </div>
    """
@app.route("/Lanciamoneta")
def lanciamoneta():
    flip = random.randint(0, 1)
    risultato = "Testa" if flip == 0 else "Croce"
    colore = "gold" if flip == 0 else "silver"
    return f"""
    <div style="text-align:center; font-family: sans-serif; margin-top: 50px;">
        <div style="width: 150px; height: 150px; background-color: {colore}; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 2em; border: 5px solid orange;">
            {risultato}
        </div>
        <br>
        <a href="/Lanciamoneta">Lancia ancora</a> | <a href="/">Torna alla home</a>
    </div>
    """

@app.route('/password') 
def genera_password():
    lunghezza = request.args.get('lunghezza', default=8, type=int)
    elements = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    for i in range(lunghezza):
        password += random.choice(elements)
    return f'<div style="text-align:center; font-family: sans-serif;"><h2>Ecco la tua password:</h2><h1 style="background-color: #eee; display: inline-block; padding: 10px;">{password}</h1><br><br><a href="/">Indietro</a></div>'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
