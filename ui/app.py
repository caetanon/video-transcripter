import sys
import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcriber import transcribe, get_available_device
from exporter import export_txt, export_srt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MODELS = ["tiny", "base", "small", "medium", "large"]

LANGUAGES = {
    "Auto-detect": "auto",
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "日本語": "ja",
    "中文": "zh",
}

VIDEO_EXTENSIONS = (
    "*.mp4", "*.mkv", "*.avi", "*.mov", "*.wmv",
    "*.flv", "*.webm", "*.m4v", "*.ts", "*.mts",
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Transcriber")
        self.geometry("820x680")
        self.minsize(700, 580)

        self._result = None
        self._is_transcribing = False

        self._build_ui()
        self._check_gpu_status()

    # ------------------------------------------------------------------ UI --

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # --- File Section ---
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=0, column=0, padx=20, pady=(20, 8), sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            file_frame, text="Arquivo de Vídeo",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 4), sticky="w")

        self.file_entry = ctk.CTkEntry(
            file_frame, placeholder_text="Selecione um arquivo de vídeo...",
        )
        self.file_entry.grid(row=1, column=0, padx=(15, 6), pady=(0, 12), sticky="ew")

        ctk.CTkButton(
            file_frame, text="Procurar", width=100, command=self._browse_file,
        ).grid(row=1, column=1, padx=(0, 15), pady=(0, 12))

        # --- Options Section ---
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=1, column=0, padx=20, pady=(0, 8), sticky="ew")
        options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            options_frame, text="Configurações",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, padx=15, pady=(12, 4), sticky="w")

        # Model
        model_col = ctk.CTkFrame(options_frame, fg_color="transparent")
        model_col.grid(row=1, column=0, padx=15, pady=(0, 14), sticky="ew")
        ctk.CTkLabel(model_col, text="Modelo Whisper").pack(anchor="w")
        self.model_var = ctk.StringVar(value="base")
        ctk.CTkOptionMenu(model_col, variable=self.model_var, values=MODELS).pack(
            fill="x", pady=(4, 0)
        )

        # Language
        lang_col = ctk.CTkFrame(options_frame, fg_color="transparent")
        lang_col.grid(row=1, column=1, padx=15, pady=(0, 14), sticky="ew")
        ctk.CTkLabel(lang_col, text="Idioma").pack(anchor="w")
        self.lang_display = ctk.StringVar(value="Auto-detect")
        ctk.CTkOptionMenu(
            lang_col, variable=self.lang_display, values=list(LANGUAGES.keys()),
        ).pack(fill="x", pady=(4, 0))

        # GPU
        gpu_col = ctk.CTkFrame(options_frame, fg_color="transparent")
        gpu_col.grid(row=1, column=2, padx=15, pady=(0, 14), sticky="ew")
        ctk.CTkLabel(gpu_col, text="Aceleração").pack(anchor="w")
        self.gpu_var = ctk.BooleanVar(value=True)
        self.gpu_check = ctk.CTkCheckBox(
            gpu_col, text="Usar GPU", variable=self.gpu_var,
        )
        self.gpu_check.pack(anchor="w", pady=(8, 0))
        self.gpu_info_label = ctk.CTkLabel(
            gpu_col, text="", font=ctk.CTkFont(size=10), text_color="gray",
        )
        self.gpu_info_label.pack(anchor="w", pady=(2, 0))

        # --- Transcribe Button ---
        self.transcribe_btn = ctk.CTkButton(
            self, text="Transcrever", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_transcription,
        )
        self.transcribe_btn.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="ew")

        # --- Transcript Area ---
        text_frame = ctk.CTkFrame(self)
        text_frame.grid(row=3, column=0, padx=20, pady=(0, 8), sticky="nsew")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            text_frame, text="Transcrição",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=15, pady=(12, 4), sticky="w")

        self.text_area = ctk.CTkTextbox(text_frame, wrap="word")
        self.text_area.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="nsew")

        # --- Bottom Bar ---
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(bottom_frame)
        self.progress_bar.grid(
            row=0, column=0, columnspan=3, padx=15, pady=(12, 6), sticky="ew"
        )
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            bottom_frame, text="Pronto.", text_color="gray",
            font=ctk.CTkFont(size=12),
        )
        self.status_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

        self.save_txt_btn = ctk.CTkButton(
            bottom_frame, text="Salvar .txt", width=115,
            state="disabled", command=self._save_txt,
        )
        self.save_txt_btn.grid(row=1, column=1, padx=(0, 6), pady=(0, 12))

        self.save_srt_btn = ctk.CTkButton(
            bottom_frame, text="Salvar .srt", width=115,
            state="disabled", command=self._save_srt,
        )
        self.save_srt_btn.grid(row=1, column=2, padx=(0, 15), pady=(0, 12))

    # ------------------------------------------------------------ Helpers --

    def _check_gpu_status(self):
        device_info = get_available_device()
        if "cpu" in device_info:
            self.gpu_info_label.configure(text="Nenhuma GPU detectada")
            self.gpu_var.set(False)
            self.gpu_check.configure(state="disabled")
        else:
            self.gpu_info_label.configure(text=device_info)

    def _set_status(self, msg: str):
        self.status_label.configure(text=msg)

    # ------------------------------------------------------- File Browse --

    def _browse_file(self):
        filetypes = [
            ("Arquivos de vídeo", " ".join(VIDEO_EXTENSIONS)),
            ("Todos os arquivos", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Selecionar vídeo", filetypes=filetypes)
        if path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, path)

    # ---------------------------------------------------- Transcription --

    def _start_transcription(self):
        if self._is_transcribing:
            return

        path = self.file_entry.get().strip()
        if not path:
            messagebox.showwarning("Atenção", "Selecione um arquivo de vídeo primeiro.")
            return
        if not Path(path).exists():
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        self._is_transcribing = True
        self._result = None

        self.transcribe_btn.configure(state="disabled", text="Transcrevendo...")
        self.save_txt_btn.configure(state="disabled")
        self.save_srt_btn.configure(state="disabled")
        self.text_area.delete("1.0", "end")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self._set_status("Iniciando...")

        thread = threading.Thread(
            target=self._run_transcription, args=(path,), daemon=True
        )
        thread.start()

    def _run_transcription(self, path: str):
        try:
            model_name = self.model_var.get()
            language = LANGUAGES.get(self.lang_display.get(), "auto")
            use_gpu = self.gpu_var.get()

            result = transcribe(
                path,
                model_name,
                language,
                use_gpu,
                status_callback=lambda msg: self.after(0, self._set_status, msg),
            )
            self.after(0, self._on_done, result)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_done(self, result: dict):
        self._result = result
        self._is_transcribing = False

        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)

        self.transcribe_btn.configure(state="normal", text="Transcrever")
        self.save_txt_btn.configure(state="normal")
        self.save_srt_btn.configure(state="normal")

        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", result["text"].strip())

        detected = result.get("language", "desconhecido")
        self._set_status(f"Concluido! Idioma detectado: {detected}")

    def _on_error(self, error: str):
        self._is_transcribing = False
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.transcribe_btn.configure(state="normal", text="Transcrever")
        self._set_status(f"Erro: {error}")
        messagebox.showerror("Erro na transcrição", error)

    # ------------------------------------------------------------ Export --

    def _save_txt(self):
        if not self._result:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            initialfile="transcricao.txt",
        )
        if path:
            export_txt(self._result, path)
            messagebox.showinfo("Salvo", f"Transcrição salva em:\n{path}")

    def _save_srt(self):
        if not self._result:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".srt",
            filetypes=[("Legenda SRT", "*.srt")],
            initialfile="transcricao.srt",
        )
        if path:
            export_srt(self._result, path)
            messagebox.showinfo("Salvo", f"Legendas salvas em:\n{path}")
