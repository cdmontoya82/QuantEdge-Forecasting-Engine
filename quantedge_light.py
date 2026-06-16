import numpy as np
import pandas as pd
from scipy.stats import poisson

def calculate_expected_goals(home_attack, away_defense, away_attack, home_defense, league_avg_goals=1.35):
    """Calcula los goles esperados de cada equipo basados en sus métricas de eficiencia."""
    home_xg = home_attack * away_defense * league_avg_goals
    away_xg = away_attack * home_defense * league_avg_goals
    return home_xg, away_xg

def compute_match_probabilities(home_xg, away_xg, max_goals=10):
    """Utiliza la distribución de Poisson para generar la matriz de probabilidades del partido."""
    home_prob_dist = [poisson.pmf(i, home_xg) for i in range(max_goals)]
    away_prob_dist = [poisson.pmf(i, away_xg) for i in range(max_goals)]
    
    # Matriz de resultados posibles
    match_matrix = np.outer(home_prob_dist, away_prob_dist)
    
    home_win_prob = np.sum(np.triu(match_matrix, 1))
    draw_prob = np.sum(np.diag(match_matrix))
    away_win_prob = np.sum(np.tril(match_matrix, -1))
    
    return home_win_prob, draw_prob, away_win_prob

def apply_kelly_criterion(internal_prob, market_odds, fraction=0.3):
    """
    Aplica el Criterio de Kelly Fraccionado para optimizar la asignación de capital.
    fraction = 0.3 (Kelly de seguridad para mitigar la varianza)
    """
    if market_odds <= 1:
        return 0
    
    # Fórmula de Kelly: (b*p - q) / b  donde b = odds - 1
    b = market_odds - 1
    p = internal_prob
    q = 1 - p
    
    raw_kelly = (b * p - q) / b
    
    # Solo apostamos si el valor esperado es positivo y Kelly > 0
    optimal_stake = max(0, raw_kelly * fraction)
    return round(optimal_stake * 100, 2) # Retorna el % del Bankroll a arriesgar

def run_quantedge_pipeline(match_data, market_odds_home):
    """Ejecuta el pipeline completo de análisis probabilístico y riesgo."""
    print("[*] Ejecutando QuantEdge-Forecasting-Engine (Version Light)...")
    
    # 1. Simular cálculo de xG (Métricas de rendimiento simuladas)
    home_xg, away_xg = calculate_expected_goals(
        match_data['home_attack'], match_data['away_defense'],
        match_data['away_attack'], match_data['home_defense']
    )
    
    # 2. Obtener probabilidades estadísticas puras
    p_home, p_draw, p_away = compute_match_probabilities(home_xg, away_xg)
    
    # 3. Calcular Valor Esperado (EV) contra el mercado
    # EV = (Probabilidad * Ganancia Potencial) - (Probabilidad de Pérdida * Capital)
    potential_profit = market_odds_home - 1
    expected_value = (p_home * potential_profit) - (1 - p_home)
    
    print("\n" + "="*50)
    print(f"📊 REPORTE DE MERCADO: {match_data['home_team']} vs {match_data['away_team']}")
    print("="*50)
    print(f"Goles Esperados (xG):       {match_data['home_team']}: {home_xg:.2f} | {match_data['away_team']}: {away_xg:.2f}")
    print(f"Probabilidad de Ganar (Model): {p_home*100:.2f}%")
    print(f"Cuota del Mercado (Odds):      {market_odds_home:.2f} (Probabilidad implícita: {1/market_odds_home*100:.2f}%)")
    print(f"Valor Esperado (EV):           {expected_value*100:.2f}%")
    
    # 4. Gestión de Riesgo si hay ventaja (Edge)
    if expected_value > 0:
        stake_percentage = apply_kelly_criterion(p_home, market_odds_home)
        print(f"🚨 ALERTA DE VENTAJA: EV Positivo detectado ({expected_value*100:.2f}%)")
        print(f"👉 Sugerencia de Inversión (Fractional Kelly): Arriesgar el {stake_percentage}% del Bankroll.")
    else:
        print("❌ SIN VENTAJA: Las cuotas del mercado absorben el valor. No operar.")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Datos de prueba de un partido ficticio de alto rendimiento
    sample_match = {
        "home_team": "Medellin FC",
        "away_team": "Bogota United",
        "home_attack": 1.4,   # 40% más efectivo que el promedio de la liga
        "away_defense": 0.8,  # Recibe 20% menos goles que el promedio
        "away_attack": 1.1,
        "home_defense": 1.2
    }
    
    # Escenario donde la casa de apuestas está pagando una cuota muy alta por error (Infracompensada)
    market_odds_home_win = 2.45 
    
    run_quantedge_pipeline(sample_match, market_odds_home_win)
