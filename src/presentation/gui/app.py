import logging

import customtkinter as ctk

from core.ai.shell import Shell

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

C = {
    "primary":       "#2563EB",
    "primary_dark":  "#1D4ED8",
    "primary_light": "#DBEAFE",
    "bg":            "#F1F5F9",
    "card":          "#FFFFFF",
    "text":          "#1E293B",
    "muted":         "#64748B",
    "ok_bg":         "#D1FAE5",
    "ok_border":     "#6EE7B7",
    "ok_fg":         "#065F46",
    "warn_bg":       "#FEF3C7",
    "warn_border":   "#FCD34D",
    "warn_fg":       "#92400E",
}
F = "Segoe UI"


class App(ctk.CTk):
    """Janela principal da aplicação de diagnóstico de arboviroses."""

    def __init__(self, yaml_path: str):
        """Inicializa a janela, o motor de inferência e constrói a interface."""
        super().__init__()
        logger.info("Inicializando interface gráfica")

        self.engine = Shell(yaml_path)
        self.title("Mini Sistema Especialista — Arboviroses")
        self.geometry("740x720")
        self.minsize(620, 500)

        self._answers: dict[str, ctk.StringVar] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._center_window()

        logger.info("Interface pronta")

    # ── centering ─────────────────────────────────────────────────────────────

    def _center_window(self):
        """Centraliza a janela na tela do usuário."""
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        """Constrói o cabeçalho azul com título e subtítulo da aplicação."""
        hdr = ctk.CTkFrame(self, corner_radius=0, fg_color=C["primary"])
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr,
            text="\U0001fa7a  Sistema de Diagnóstico de Arboviroses",
            font=ctk.CTkFont(F, 17, "bold"),
            text_color="white",
        ).grid(row=0, column=0, pady=(18, 4))

        ctk.CTkLabel(
            hdr,
            text="Responda as perguntas sobre os sintomas do paciente",
            font=ctk.CTkFont(F, 11),
            text_color=C["primary_light"],
        ).grid(row=1, column=0, pady=(0, 18))

    # ── body ──────────────────────────────────────────────────────────────────

    def _build_body(self):
        """Constrói o corpo da janela com a lista de perguntas, botões e área de resultado."""
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="Sintomas do Paciente",
            font=ctk.CTkFont(F, 13, "bold"),
            text_color=C["text"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        scroll = ctk.CTkScrollableFrame(
            body, fg_color=C["bg"], corner_radius=8,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8",
        )
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        for i, (fact, question) in enumerate(self.engine.questions.items()):
            self._build_question_card(scroll, i, fact, question)

        self._build_buttons(body)
        self._build_results(body)

    # ── question card ─────────────────────────────────────────────────────────

    def _build_question_card(self, parent, index: int, fact: str, question: str):
        """Cria um card com toggle Sim/Não para um sintoma."""
        var = ctk.StringVar(value="nao")
        self._answers[fact] = var

        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=8)
        card.grid(row=index, column=0, sticky="ew", pady=3, padx=2)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text=f"{index + 1:02d}",
            font=ctk.CTkFont(F, 9, "bold"),
            fg_color=C["primary_light"],
            text_color=C["primary"],
            corner_radius=4,
            width=28, height=20,
        ).grid(row=0, column=0, padx=(12, 0), pady=14, sticky="n")

        ctk.CTkLabel(
            card,
            text=question,
            font=ctk.CTkFont(F, 11),
            text_color=C["text"],
            anchor="w",
            justify="left",
            wraplength=420,
        ).grid(row=0, column=1, padx=(10, 8), pady=14, sticky="w")

        toggle_frame = ctk.CTkFrame(card, fg_color="transparent")
        toggle_frame.grid(row=0, column=2, padx=(0, 16), pady=14)

        ctk.CTkLabel(
            toggle_frame,
            text="Não",
            font=ctk.CTkFont(F, 11),
            text_color=C["muted"],
        ).pack(side="left", padx=(0, 6))

        ctk.CTkSwitch(
            toggle_frame,
            text="Sim",
            font=ctk.CTkFont(F, 11),
            variable=var,
            onvalue="sim",
            offvalue="nao",
            progress_color=C["primary"],
            button_color=C["primary_dark"],
            button_hover_color=C["primary"],
            command=lambda f=fact: self._on_toggle(f),
        ).pack(side="left")

    def _on_toggle(self, fact: str):
        """Registra no log o estado do toggle quando o usuário interage."""
        state = self._answers[fact].get()
        logger.debug("Sintoma '%s' → %s", fact, state)

    # ── buttons ───────────────────────────────────────────────────────────────

    def _build_buttons(self, parent):
        """Adiciona os botões Diagnosticar e Reiniciar ao rodapé do corpo."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.grid(row=2, column=0, sticky="w", pady=14)

        ctk.CTkButton(
            row,
            text="\U0001f50d  Diagnosticar",
            command=self._run_diagnosis,
            font=ctk.CTkFont(F, 12, "bold"),
            corner_radius=8,
            height=38,
            fg_color=C["primary"],
            hover_color=C["primary_dark"],
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            row,
            text="\u21ba  Reiniciar",
            command=self._reset,
            font=ctk.CTkFont(F, 12),
            corner_radius=8,
            height=38,
            fg_color="#E2E8F0",
            text_color=C["text"],
            hover_color="#CBD5E1",
        ).pack(side="left")

    # ── results ───────────────────────────────────────────────────────────────

    def _build_results(self, parent):
        """Cria o container oculto que exibirá os cards de resultado."""
        self._result_container = ctk.CTkFrame(parent, fg_color="transparent")

        ctk.CTkLabel(
            self._result_container,
            text="Resultado do Diagnóstico",
            font=ctk.CTkFont(F, 13, "bold"),
            text_color=C["text"],
        ).pack(anchor="w", pady=(0, 6))

        self._result_inner = ctk.CTkFrame(
            self._result_container, fg_color="transparent"
        )
        self._result_inner.pack(fill="x")

    def _result_card(self, text: str, alert: bool = False):
        """Renderiza um card de resultado com estilo verde (diagnóstico) ou amarelo (alerta)."""
        is_alert = alert or str(text).lower().startswith("alerta")
        bg, border, fg = (
            (C["warn_bg"],  C["warn_border"],  C["warn_fg"])
            if is_alert else
            (C["ok_bg"],   C["ok_border"],    C["ok_fg"])
        )
        icon = "\u26a0\ufe0f" if is_alert else "\u2705"

        card = ctk.CTkFrame(
            self._result_inner,
            fg_color=bg,
            corner_radius=8,
            border_color=border,
            border_width=1,
        )
        card.pack(fill="x", pady=3)

        ctk.CTkLabel(
            card,
            text=f"{icon}  {text}",
            font=ctk.CTkFont(F, 11),
            text_color=fg,
            justify="left",
            anchor="w",
            wraplength=640,
        ).pack(anchor="w", padx=14, pady=10)

    # ── logic ─────────────────────────────────────────────────────────────────

    def _run_diagnosis(self):
        """Coleta respostas marcadas, executa a inferência e exibe os diagnósticos."""
        self.engine.facts     = set()
        self.engine.diagnoses = []

        for fact, var in self._answers.items():
            if var.get() == "sim":
                self.engine.facts.add(fact)

        logger.info(
            "Diagnóstico solicitado | sintomas marcados: %s",
            list(self.engine.facts),
        )

        self.engine._infer_facts()

        for widget in self._result_inner.winfo_children():
            widget.destroy()

        if self.engine.diagnoses:
            for diagnosis in self.engine.diagnoses:
                self._result_card(diagnosis)
        else:
            logger.warning("Nenhum diagnóstico identificado para os sintomas informados")
            self._result_card(
                "Nenhum diagnóstico identificado com os sintomas informados.",
                alert=True,
            )

        self._result_container.grid(row=3, column=0, sticky="ew")

    def _reset(self):
        """Redefine todos os toggles para 'não' e oculta o container de resultados."""
        logger.info("Formulário reiniciado pelo usuário")
        for var in self._answers.values():
            var.set("nao")
        self._result_container.grid_forget()

    # ── entry ─────────────────────────────────────────────────────────────────

    def run(self):
        """Inicia o loop principal da interface gráfica."""
        logger.info("Iniciando loop principal")
        self.mainloop()
        logger.info("Interface encerrada")
