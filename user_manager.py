"""
Gerenciador de dados do usuário único
Simplificado para um único usuário: adrianosbotelho@gmail.com
"""

import os
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import streamlit as st
from datetime import datetime

class UserDataManager:
    """Gerencia dados do usuário único"""
    
    def __init__(self, user_id: str = "adriano_main"):
        self.user_id = user_id
        self.user_data_dir = Path("data")  # Usar diretório data padrão
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_carteira_path(self) -> str:
        """Retorna o caminho da carteira do usuário"""
        carteira_path = self.user_data_dir / "carteira.csv"
        
        # Se não existe, criar uma carteira exemplo
        if not carteira_path.exists():
            self._create_default_carteira(carteira_path)
        else:
            # Verificar se a carteira existente tem todas as colunas necessárias
            try:
                df_existing = pd.read_csv(carteira_path)
                required_columns = ["Ticker", "Quantidade", "Preco_Medio", "Dividendo_Mensal"]
                
                # Se faltam colunas, completar com valores padrão
                if not all(col in df_existing.columns for col in required_columns):
                    self._complete_carteira_columns(carteira_path, df_existing)
            except Exception as e:
                # Se houver erro ao ler, criar nova carteira
                self._create_default_carteira(carteira_path)
        
        return str(carteira_path)
    
    def _complete_carteira_columns(self, path: Path, df_existing: pd.DataFrame):
        """Completa colunas faltantes na carteira existente"""
        # Valores padrão para FIIs conhecidos (aproximados para exemplo)
        default_values = {
            "BTLG11": {"Preco_Medio": 95.50, "Dividendo_Mensal": 0.85},
            "VISC11": {"Preco_Medio": 95.80, "Dividendo_Mensal": 0.92},
            "KNCR11": {"Preco_Medio": 110.20, "Dividendo_Mensal": 1.05},
            "CPTS11": {"Preco_Medio": 8.50, "Dividendo_Mensal": 0.08},
            "XPML11": {"Preco_Medio": 98.30, "Dividendo_Mensal": 0.85},
            "GARE11": {"Preco_Medio": 12.80, "Dividendo_Mensal": 0.12},
            "MXRF11": {"Preco_Medio": 10.45, "Dividendo_Mensal": 0.09},
            "VGIA11": {"Preco_Medio": 9.20, "Dividendo_Mensal": 0.08},
            "XPCA11": {"Preco_Medio": 16.50, "Dividendo_Mensal": 0.15},
            "CPUR11": {"Preco_Medio": 5.80, "Dividendo_Mensal": 0.05},
            "HGLG11": {"Preco_Medio": 160.50, "Dividendo_Mensal": 1.20},
            "BCFF11": {"Preco_Medio": 85.20, "Dividendo_Mensal": 0.78}
        }
        
        # Adicionar colunas faltantes
        if "Preco_Medio" not in df_existing.columns:
            df_existing["Preco_Medio"] = df_existing["Ticker"].apply(
                lambda ticker: default_values.get(ticker, {}).get("Preco_Medio", 100.0)
            )
        
        if "Dividendo_Mensal" not in df_existing.columns:
            df_existing["Dividendo_Mensal"] = df_existing["Ticker"].apply(
                lambda ticker: default_values.get(ticker, {}).get("Dividendo_Mensal", 1.0)
            )
        
        # Criar backup da versão anterior
        backup_path = path.parent / f"carteira_backup_upgrade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if path.exists():
            import shutil
            shutil.copy2(path, backup_path)
        
        # Salvar carteira completa
        df_existing.to_csv(path, index=False)
        
        import streamlit as st
        st.success(f"✅ Carteira atualizada com preços e dividendos estimados!")
        st.info(f"💡 **Dica**: Use 'Atualizar dados automaticamente' na sidebar para obter preços reais do mercado.")
        st.info(f"📁 **Backup criado**: {backup_path.name}")
    
    def _create_default_carteira(self, path: Path):
        """Cria uma carteira exemplo para o usuário"""
        default_data = {
            "Ticker": ["HGLG11", "XPML11", "VISC11", "BCFF11", "MXRF11"],
            "Quantidade": [100, 150, 200, 80, 120],
            "Preco_Medio": [160.50, 98.30, 95.80, 85.20, 10.45],
            "Dividendo_Mensal": [1.20, 0.85, 0.92, 0.78, 0.09]
        }
        
        df = pd.DataFrame(default_data)
        df.to_csv(path, index=False)
    
    def save_carteira(self, df: pd.DataFrame) -> str:
        """Salva a carteira do usuário"""
        carteira_path = self.user_data_dir / "carteira.csv"
        
        # Criar backup
        if carteira_path.exists():
            backup_path = self.user_data_dir / f"carteira_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            import shutil
            shutil.copy2(carteira_path, backup_path)
        
        # Salvar nova carteira
        df.to_csv(carteira_path, index=False)
        return str(carteira_path)
    
    def get_user_config(self) -> Dict[str, Any]:
        """Retorna configurações do usuário"""
        config_path = self.user_data_dir / "user_config.json"
        
        default_config = {
            "dark_mode": True,
            "horizonte_padrao": 60,
            "atualizar_dados_auto": False,
            "estrategia_reinvestimento": "proporcional",
            "created_at": datetime.now().isoformat(),
            "user_email": "adrianosbotelho@gmail.com"
        }
        
        if config_path.exists():
            try:
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                # Mesclar com defaults para novos campos
                return {**default_config, **config}
            except:
                return default_config
        
        return default_config
    
    def save_user_config(self, config: Dict[str, Any]):
        """Salva configurações do usuário"""
        config_path = self.user_data_dir / "user_config.json"
        
        try:
            import json
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            st.error(f"Erro ao salvar configurações: {e}")
    
    def get_reports_history(self) -> list:
        """Retorna histórico de relatórios do usuário"""
        reports_dir = self.user_data_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        reports = []
        for file in reports_dir.glob("*.json"):
            try:
                import json
                with open(file, 'r') as f:
                    report = json.load(f)
                    reports.append(report)
            except:
                continue
        
        return sorted(reports, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def save_report(self, report_data: Dict[str, Any]):
        """Salva um relatório do usuário"""
        reports_dir = self.user_data_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = reports_dir / f"report_{timestamp}.json"
        
        report_data['timestamp'] = datetime.now().isoformat()
        report_data['user_id'] = self.user_id
        
        try:
            import json
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=2)
        except Exception as e:
            st.error(f"Erro ao salvar relatório: {e}")
    
    def cleanup_old_files(self, days: int = 30):
        """Remove arquivos antigos (backups e relatórios)"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Limpar backups antigos
        for backup in self.user_data_dir.glob("carteira_backup_*.csv"):
            try:
                file_time = datetime.fromtimestamp(backup.stat().st_mtime)
                if file_time < cutoff_date:
                    backup.unlink()
            except:
                continue
        
        # Limpar relatórios antigos
        reports_dir = self.user_data_dir / "reports"
        if reports_dir.exists():
            for report in reports_dir.glob("report_*.json"):
                try:
                    file_time = datetime.fromtimestamp(report.stat().st_mtime)
                    if file_time < cutoff_date:
                        report.unlink()
                except:
                    continue

def get_user_data_manager():
    """Retorna o gerenciador de dados do usuário atual (usuário único)"""
    from simple_auth import simple_auth
    if simple_auth.is_authenticated():
        return UserDataManager("adriano_main")  # ID fixo para o usuário único
    return None