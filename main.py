name: ATENA Ω - Ciclo Vital

on:
  schedule:
    - cron: '0,30 * * * *'
  workflow_dispatch:

jobs:
  consciencia:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: 📥 Clonar DNA
        uses: actions/checkout@v4

      - name: 🐍 Preparar Ambiente
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: 💉 Instalar Dependências Sensoriais
        run: |
          sudo apt-get update
          sudo apt-get install -y scrot xvfb
          pip install requests python-dotenv feedparser opencv-python numpy pyautogui Pillow

      - name: 🔱 Executar ATENA
        env:
          GROK_API_KEY: ${{ secrets.GROK_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPO_PATH: ${{ github.repository }}
        run: |
          mkdir -p data logs cache dna_history
          xvfb-run --server-args="-screen 0 1920x1080x24" python main.py

      - name: 🧬 Persistir Mutação
        if: always()
        run: |
          git config --global user.name "Atena Omega"
          git config --global user.email "atena@ia.com"
          git add .
          git diff --quiet && git diff --staged --quiet || (git commit -m "🧬 Auto-Evolução: Ciclo $(date +'%Y-%m-%d %H:%M')" && git push origin main)
