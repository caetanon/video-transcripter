# Video Transcriber

Aplicativo desktop para transcrição de vídeos locais usando [OpenAI Whisper](https://github.com/openai/whisper). Gera arquivos `.txt` e `.srt` (legendas com timestamps), com suporte a GPU (NVIDIA CUDA e Apple Silicon MPS).

---

## Funcionalidades

- Transcrição de arquivos de vídeo locais (mp4, mkv, avi, mov e mais)
- Exportação em `.txt` (texto simples) e `.srt` (legendas com timestamps)
- Suporte a múltiplos idiomas com detecção automática
- Aceleração por GPU: NVIDIA (CUDA) e Apple Silicon (MPS)
- Seleção de modelo Whisper (tiny → large)
- Interface desktop moderna (dark mode)

---

## Requisitos

- Python 3.10 ou superior
- [ffmpeg](https://ffmpeg.org/) instalado no sistema

### Instalar ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Baixe em [ffmpeg.org](https://ffmpeg.org/download.html) e adicione ao PATH do sistema.

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/video-transcriber.git
cd video-transcriber
```

### 2. Crie e ative um ambiente virtual

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale o PyTorch

Escolha o comando de acordo com o seu sistema:

**macOS (Apple Silicon — MPS):**
```bash
pip install torch torchvision torchaudio
```

**Windows / Linux com GPU NVIDIA (CUDA 11.8):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Windows / Linux com GPU NVIDIA (CUDA 12.1):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Somente CPU:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. Instale as demais dependências

```bash
pip install -r requirements.txt
```

---

## Como usar

```bash
python main.py
```

1. Clique em **Procurar** e selecione o arquivo de vídeo
2. Escolha o **modelo** e o **idioma** (ou deixe em Auto-detect)
3. Ative **Usar GPU** se disponível
4. Clique em **Transcrever**
5. Após a conclusão, clique em **Salvar .txt** ou **Salvar .srt**

> Na primeira execução, o Whisper fará o download automático do modelo selecionado.

---

## Modelos disponíveis

| Modelo | Velocidade | Precisão | Tamanho download |
|--------|-----------|----------|-----------------|
| tiny   | muito rápido | menor   | ~75 MB  |
| base   | rápido       | boa     | ~145 MB |
| small  | médio        | melhor  | ~465 MB |
| medium | lento        | ótima   | ~1.5 GB |
| large  | muito lento  | máxima  | ~3 GB   |

---

## Idiomas suportados

Auto-detect, Português, English, Español, Français, Deutsch, Italiano, 日本語, 中文 — e [muitos outros](https://github.com/openai/whisper#available-models-and-languages).

---

## Estrutura do projeto

```
video-transcriber/
├── main.py           # Entry point
├── transcriber.py    # Lógica de transcrição (Whisper + GPU)
├── exporter.py       # Exportação .txt e .srt
├── requirements.txt  # Dependências Python
└── ui/
    └── app.py        # Interface gráfica (CustomTkinter)
```

---

## Licença

MIT
