<!-- PROJECT -->
<h1 align="center" style="font-weight: bold;">Monitorando – Sistema de Mentorias 🎓</h1>

<p align="center">
  <!-- Adicione aqui os badges das tecnologias que você usou -->
  <img src="https://img.shields.io/badge/Deployed%20on-Render-00979D?logo=render&style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
</p>

<p align="center">
  <a href="#-descrição">Descrição</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-como-executar-localmente">Como Executar</a> •
  <a href="#️-demonstrações-capturas-de-tela">Demonstrações</a> •
  <a href="https://plataforma-mentorados.onrender.com/usuarios/login/">Ver na Web</a>

</p>

---

## 📌 Descrição

**Monitorando** é um sistema completo para gerenciamento de mentorias, desenvolvido com **Python** e **Django**. O projeto, criado durante a PyStack Week 13, simula uma plataforma onde mentores podem organizar tarefas e disponibilizar conteúdos, enquanto mentorados acessam materiais exclusivos de forma segura através de um token.

A plataforma inclui funcionalidades essenciais como upload de vídeos, gerenciamento de reuniões e painéis de controle distintos para mentores e mentorados, oferecendo uma experiência de usuário organizada e eficiente.

---

## 🚀 Funcionalidades

- **Autenticação Segura:** Sistema completo de login e registro de usuários.
- **Agendamento de Mentorias:** Ferramentas para marcar e visualizar encontros.
- **Conteúdo Exclusivo:** Upload e visualização de gravações e materiais.
- **Acesso Restrito:** Mentorados acessam o conteúdo através de um token exclusivo.
- **Painel do Mentor:** Área administrativa para gerenciamento de tarefas e mentorados.
- **Arquitetura Modular:** Código organizado com views e templates separados para fácil manutenção.

---

## 🔒 Destaques Técnicos

- **Segurança com Tokens:** Implementação de tokens únicos para garantir o acesso restrito dos mentorados aos conteúdos.
- **Arquitetura Django:** Utilização da arquitetura MVT (Model-View-Template) para criar um sistema modular e escalável.
- **Upload de Arquivos:** Sistema seguro para upload de vídeos e outros materiais, com armazenamento gerenciado pelo Django.
- **Design Responsivo:** Interface adaptável a diferentes dispositivos, construída com HTML5 e CSS3.
- **Banco de Dados Flexível:** Desenvolvido com SQLite para simplicidade, mas com suporte nativo para migração para bancos como PostgreSQL.

---

## 🚀 Como Executar Localmente

Siga as instruções abaixo para executar o projeto em seu ambiente local.

### Pré-requisitos

- [Python](https://www.python.org/downloads/) (versão 3.8 ou superior)
- [Git](https://git-scm.com/)

### Clonando o Repositório

```bash
# Clone o projeto para a sua máquina local
git clone https://github.com/MarissaBorges/PystackWeek13

# Entre no diretório do projeto
cd PystackWeek13
```

### Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente
# No Windows:
.venv\\Scripts\\activate

# No macOS/Linux:
source .venv/bin/activate
```

### Instale as Dependências

Com o **ambiente virtual ativo**, use o arquivo `requirements.txt` para instalar as dependências.

```bash
# Instale todas as bibliotecas necessárias
pip install -r requirements.txt
```

### Migrações do Banco de Dados

Aplique as migrações para configurar o banco de dados.

```bash
# Crie as tabelas no banco de dados
python projeto_pythonando/manage.py makemigrations mentorados
```

### Crie um Superusuário

Para acessar o painel administrativo do Django, crie um superusuário.

```bash
# Crie um usuário administrador
python projeto_pythonando/manage.py createsuperuser
```

### Iniciando o Projeto

Forneça o comando exato para iniciar a aplicação.

```bash
# Inicie o servidor de desenvolvimento
python projeto_pythonando/manage.py runserver
```

### Como Interagir

- Acesse a aplicação em seu navegador: `http://127.0.0.1:8000/usuarios/login/`
- Utilize a tela de registro para criar uma conta de mentor ou mentorado.
- Acesse o painel administrativo em `http://127.0.0.1:8000/admin` com as credenciais do superusuário.

---

## 🖼️ Demonstrações (capturas de tela)

![Tela de Login](https://i.postimg.cc/N0XfGgW4/image.png)
_Tela de autenticação de usuários._

![Dashboard do Mentor](https://i.postimg.cc/pX9NM0NQ/image.png)
_Painel principal onde o mentor gerencia suas atividades._

---

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MarissaBorges">
        <img src="https://github.com/MarissaBorges.png?size=100" width="100px;" alt="Foto de Marissa Borges"/><br>
        <sub>
          <b>Marissa Borges</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

## 📫 Como Contribuir

1.  Faça um **Fork** do projeto.
2.  Crie uma nova branch para sua Feature (`git checkout -b feature/AmazingFeature`).
3.  Faça o **Commit** de suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4.  Faça o **Push** da sua branch (`git push origin feature/AmazingFeature`).
5.  Abra um **Pull Request**.

### Documentações Úteis

- [📝 Como criar um Pull Request](https://www.atlassian.com/br/git/tutorials/making-a-pull-request)
- [💾 Padrão de Commits (Conventional Commits)](https://www.conventionalcommits.org/en/v1.0.0/)
