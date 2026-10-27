"use strict";

const URL_API = "/api/v1/autenticacao";

const telaLogin = document.getElementById("tela-login");
const telaSucesso = document.getElementById("tela-sucesso");
const form = document.getElementById("form-login");
const campoIdentificador = document.getElementById("identificador");
const campoSenha = document.getElementById("senha");
const botaoEntrar = document.getElementById("botao-entrar");
const botaoMostrar = document.getElementById("mostrar-senha");
const avisoCaps = document.getElementById("senha-caps");
const alerta = document.getElementById("alerta");
const alertaTexto = document.getElementById("alerta-texto");

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  esconderAlerta();

  if (!validarCampos()) {
    return;
  }

  carregando(true);
  try {
    const resposta = await fetch(URL_API, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        identificador: campoIdentificador.value,
        senha: campoSenha.value,
      }),
    });

    if (resposta.ok) {
      const dados = await resposta.json();
      mostrarSucesso(dados.usuario);
      return;
    }

    mostrarAlerta(await mensagemDeErro(resposta));
    if (resposta.status === 401) {
      campoSenha.value = "";
      campoSenha.focus();
    }
  } catch {
    mostrarAlerta("Não foi possível falar com o servidor. Verifique sua conexão e tente de novo.");
  } finally {
    carregando(false);
  }
});

async function mensagemDeErro(resposta) {
  if (resposta.status === 429) {
    const segundos = Number(resposta.headers.get("Retry-After"));
    if (segundos > 0) {
      return `Muitas tentativas seguidas. Aguarde ${segundos} segundos e tente de novo.`;
    }
  }

  // os erros da API vêm no formato Problem Details, com a mensagem no campo "detail"
  try {
    const problema = await resposta.json();
    if (problema.detail) {
      return problema.detail;
    }
  } catch {
    // corpo vazio ou que não é JSON
  }
  return "Algo deu errado. Tente novamente em instantes.";
}

/* ---------- validação ---------- */

function validarCampos() {
  const identificadorOk = validarCampo(campoIdentificador, "Informe seu login ou e-mail.");
  const senhaOk = validarCampo(campoSenha, "Informe sua senha.");

  if (!identificadorOk) {
    campoIdentificador.focus();
  } else if (!senhaOk) {
    campoSenha.focus();
  }
  return identificadorOk && senhaOk;
}

function validarCampo(campo, mensagem) {
  const vazio = campo.value.trim() === "";
  definirErro(campo, vazio ? mensagem : "");
  return !vazio;
}

function definirErro(campo, mensagem) {
  document.getElementById(`${campo.id}-erro`).textContent = mensagem;
  if (mensagem) {
    campo.setAttribute("aria-invalid", "true");
  } else {
    campo.removeAttribute("aria-invalid");
  }
}

for (const campo of [campoIdentificador, campoSenha]) {
  campo.addEventListener("input", () => definirErro(campo, ""));
}

/* ---------- senha ---------- */

botaoMostrar.addEventListener("click", () => {
  const mostrando = campoSenha.type === "text";
  campoSenha.type = mostrando ? "password" : "text";
  botaoMostrar.textContent = mostrando ? "Mostrar" : "Ocultar";
  botaoMostrar.setAttribute("aria-pressed", String(!mostrando));
  campoSenha.focus();
});

for (const tipo of ["keydown", "keyup"]) {
  campoSenha.addEventListener(tipo, (evento) => {
    if (evento.getModifierState) {
      avisoCaps.hidden = !evento.getModifierState("CapsLock");
    }
  });
}
campoSenha.addEventListener("blur", () => {
  avisoCaps.hidden = true;
});

/* ---------- estados da tela ---------- */

function carregando(ativo) {
  botaoEntrar.disabled = ativo;
  botaoEntrar.classList.toggle("carregando", ativo);
  botaoEntrar.querySelector(".botao-rotulo").textContent = ativo ? "Entrando…" : "Entrar";
}

function mostrarAlerta(mensagem) {
  // textContent, nunca innerHTML: o texto vem do servidor
  alertaTexto.textContent = mensagem;
  alerta.hidden = false;
}

function esconderAlerta() {
  alerta.hidden = true;
  alertaTexto.textContent = "";
}

function mostrarSucesso(usuario) {
  document.getElementById("usuario-nome").textContent = primeiroNome(usuario.nome);
  document.getElementById("usuario-login").textContent = usuario.login;
  document.getElementById("usuario-email").textContent = usuario.email;
  document.getElementById("usuario-id").textContent = usuario.id;
  document.getElementById("avatar").textContent = iniciais(usuario.nome);

  form.reset();
  campoSenha.type = "password";
  botaoMostrar.textContent = "Mostrar";
  botaoMostrar.setAttribute("aria-pressed", "false");

  telaLogin.hidden = true;
  telaSucesso.hidden = false;
  document.getElementById("sucesso-titulo").focus();
}

document.getElementById("voltar").addEventListener("click", () => {
  telaSucesso.hidden = true;
  telaLogin.hidden = false;
  campoIdentificador.focus();
});

function primeiroNome(nome) {
  return nome.trim().split(/\s+/)[0];
}

function iniciais(nome) {
  const partes = nome.trim().split(/\s+/);
  const primeira = partes[0][0];
  const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";
  return (primeira + ultima).toUpperCase();
}
