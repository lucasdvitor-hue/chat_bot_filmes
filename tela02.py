import customtkinter
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

# --- Configurações de Cores ---
co0 = "#0E5271" # azul
co1 = "#feffff" # branco
co6 = "#03091f" # azul escuro (fundo)
co_btn = "#e06636" # Laranja para destaque

# --- Lógica do Chatbot (Backend) ---
def buscar_recomendacao():
    frase = entry_sentimento.get()
    
    if not frase:
        label_status.configure(text="Digite algo!")
        return

    # Análise de Sentimento
    analyzer = SentimentIntensityAnalyzer()
    emotion = analyzer.polarity_scores(frase)['compound']
    
    # Define o Gênero
    if emotion <= -0.5:
        genre_id = '18' # Drama
        nome_genero = "Drama"
    elif emotion < 0:
        genre_id = '35' # Comédia
        nome_genero = "Comédia"
    elif emotion < 0.5:
        genre_id = '10749' # Romance
        nome_genero = "Romance"
    else:
        genre_id = '27' # Terror
        nome_genero = "Terror"

    label_status.configure(text=f"Gênero: {nome_genero} | Score: {emotion:.2f}")

    # --- ALEATORIEDADE PARTE 1: Sorteia a página ---
    # Em vez de pegar sempre a página 1 (Top 20), pegamos qualquer uma entre 1 e 10
    pagina_aleatoria = random.randint(1, 10)

    # Use a SUA chave que funcionou no teste anterior
    api_key = 'ca145e8ff9bcfbaa1f8939ada2d484c6' 
    
    # Note o final da URL: &page={pagina_aleatoria}
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&sort_by=popularity.desc&with_genres={genre_id}&vote_count.gte=100&page={pagina_aleatoria}"

    try:
        response = requests.get(url)
        dados = response.json()
        
        texto_final = ""
        
        if 'results' in dados:
            filmes = dados['results']
            
            # --- ALEATORIEDADE PARTE 2: Embaralha a lista ---
            # Mesmo se cair na mesma página, a ordem muda
            random.shuffle(filmes)

            # Pega os 5 primeiros da lista JÁ embaralhada
            for filme in filmes[:5]:
                titulo = filme['title']
                nota = filme['vote_average']
                texto_final += f"🎬 {titulo} - ⭐ {nota}\n\n"
        else:
            texto_final = "Nenhum filme encontrado."

        textbox_resultado.delete("0.0", "end")
        textbox_resultado.insert("0.0", texto_final)
        
    except Exception as e:
        textbox_resultado.delete("0.0", "end")
        textbox_resultado.insert("0.0", f"Erro: {e}")

# --- Interface Gráfica (Frontend) ---

customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("blue")

janela = customtkinter.CTk()
janela.title('CineMood AI')
janela.geometry('500x600')

# Frame Cabeçalho
frameCima = customtkinter.CTkFrame(janela, width=500, height=60, corner_radius=0, fg_color=co6)
frameCima.pack(fill="x")
label_titulo = customtkinter.CTkLabel(frameCima, text="🤖 CineMood AI", font=("Arial", 20, "bold"), text_color="white")
label_titulo.place(relx=0.5, rely=0.5, anchor="center")

# Frame Pergunta
frameAsk = customtkinter.CTkFrame(janela, fg_color="transparent")
frameAsk.pack(pady=20, padx=20, fill="x")

label_ask = customtkinter.CTkLabel(frameAsk, text="Como você está se sentindo hoje?", font=("Arial", 14))
label_ask.pack(anchor="w")

entry_sentimento = customtkinter.CTkEntry(frameAsk, placeholder_text="Ex: Estou cansado e um pouco triste...", width=300)
entry_sentimento.pack(pady=10, fill="x")

btn_recomendar = customtkinter.CTkButton(frameAsk, text="Recomendar Filmes", command=buscar_recomendacao, fg_color=co_btn, hover_color="#c4552b")
btn_recomendar.pack(fill="x")

# Frame Resultado
frameResultado = customtkinter.CTkFrame(janela, fg_color="transparent")
frameResultado.pack(pady=10, padx=20, fill="both", expand=True)

label_status = customtkinter.CTkLabel(frameResultado, text="", text_color="gray")
label_status.pack()

# Caixa de Texto para os filmes (Melhor que label para listas)
textbox_resultado = customtkinter.CTkTextbox(frameResultado, font=("Arial", 16))
textbox_resultado.pack(fill="both", expand=True)

janela.mainloop()