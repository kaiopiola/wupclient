# WupClient GUI Mod

## Novidades / Melhorias

- **Delete Recursivo**: Agora é possível apagar pastas e todo o seu conteúdo (inclusive subpastas e arquivos) de forma recursiva diretamente pela interface. Basta selecionar a pasta e, ao confirmar a exclusão, digitar `ALL` para que a remoção seja feita de forma completa, mesmo para pastas não vazias.
- Outras melhorias de usabilidade e compatibilidade.

## Sobre

Este projeto é uma interface gráfica (GUI) em Python para o `wupclient`, permitindo explorar, transferir, instalar e gerenciar arquivos do Wii U remotamente via rede. Baseado em scripts clássicos da comunidade homebrew, com melhorias para uso moderno.

## Requisitos

- **Wii U** com wupserver (fw.img) rodando
- **Python 2.7** (não funciona em Python 3)
  - Baixe em: https://www.python.org/downloads/release/python-2718/
- Windows (recomendado)

## Instalação do Python 2.7

1. Baixe o instalador do Python 2.7: [Python 2.7.18 Windows x86-64 MSI installer](https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi)
2. Instale normalmente, marcando a opção para instalar o Tcl/Tk (Tkinter).
3. (Opcional) Adicione `C:\Python27` ao PATH do Windows.

## Como executar o WupClient GUI

1. **Abra o Prompt de Comando ou PowerShell na pasta do projeto.**
2. Execute:
   ```
   C:\Python27\python.exe wupclientgui.py
   ```
   ou, se Python 2.7 estiver no PATH:
   ```
   python wupclientgui.py
   ```
3. Na interface, clique em "Connect" e digite o IP do seu Wii U (com wupserver rodando).

## Funções da Interface

- **Connect**: conecta ao Wii U pelo IP informado.
- **Refresh**: atualiza a listagem do diretório atual.
- **Mount usb / Mount odd_tickets / Unmount odd_tickets**: monta/desmonta volumes do Wii U.
- **Download Folder**: baixa uma pasta do Wii U para o PC.
- **Create Folder**: cria uma nova pasta no Wii U.
- **Install Title**: instala um título a partir de uma pasta selecionada.
- **Copy / Paste**: copia e cola arquivos entre Wii U e PC.
- **Delete File**: apaga um arquivo selecionado.
- **Delete Folder**: apaga uma pasta selecionada. Se digitar `ALL` na confirmação, apaga recursivamente (inclusive pastas não vazias).
  - **Delete Recursivo**: Ao digitar `ALL` na confirmação, a exclusão será feita de forma recursiva, removendo todos os arquivos e subpastas.

## Observações

- O app só funciona com Python 2.7 devido à dependência do Tkinter antigo e sintaxe.
- Para deletar pastas não vazias, digite `ALL` na confirmação.
  - Com a opção de delete recursivo, todo o conteúdo da pasta será removido permanentemente.
- O Wii U e o PC devem estar na mesma rede.

## Créditos
- Smea, FIX94, CreeperMario, Maschell, rw-r-r_0644, vgmoose e comunidade homebrew Wii U.

---

Se encontrar bugs ou quiser contribuir, abra uma issue ou envie um pull request!
