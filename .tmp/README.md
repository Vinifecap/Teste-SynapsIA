# 📁 Arquivos Temporários

Este diretório contém arquivos intermediários gerados durante o processamento.

## Regras

- **NUNCA commitar** este diretório no Git
- Todo conteúdo pode ser **deletado e regenerado**
- Usado para: dados scraped, exports temporários, dossiers, cache local
- Deliverables finais vão para serviços de nuvem (Google Sheets, Slides, etc.)

## Limpeza

Para limpar todos os arquivos temporários:
```bash
rm -rf .tmp/*
```
