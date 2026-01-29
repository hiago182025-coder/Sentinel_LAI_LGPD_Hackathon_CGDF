# Arquivo: generate_data.py
from src.data_generator import LaiDataGenerator
import os

def main():
    print(">> Gerando dataset massivo...")
    # Cria pasta se não existir
    os.makedirs('data/raw', exist_ok=True)
    
    # Gera 2000 exemplos
    gen = LaiDataGenerator()
    df = gen.generate(2000)
    
    # Salva
    output_path = 'data/raw/dataset_gigante_lai.csv'
    df.to_csv(output_path, index=False)
    print(f">> Sucesso! Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    main()
