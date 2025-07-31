import numpy as np
import pandas as pd
from possession_simulator import simulate_possession

# Intensity mapping (from PDF pages 10-11)
ACTION_INTENSITY = {
    "static": {"hr_change": -1, "speed": 0.5, "accel": 0.1, "pl": 0.01},
    "ball hold": {"hr_change": 0, "speed": 0.5, "accel": 0.1, "pl": 0.01},
    "walk": {"hr_change": 1, "speed": 1.2, "accel": 0.2, "pl": 0.02},
    "jog": {"hr_change": 2, "speed": 3.0, "accel": 0.5, "pl": 0.05},
    "dribble": {"hr_change": 3, "speed": 3.5, "accel": 1.0, "pl": 0.1},
    "cut": {"hr_change": 4, "speed": 5.5, "accel": 2.5, "pl": 0.2},
    "sprint": {"hr_change": 5, "speed": 6.5, "accel": 3.5, "pl": 0.3},
    "roll": {"hr_change": 4, "speed": 5.0, "accel": 3.0, "pl": 0.25},
    "drive": {"hr_change": 5, "speed": 6.0, "accel": 3.5, "pl": 0.3},
    "on-ball screen": {"hr_change": 2, "speed": 1.0, "accel": 0.5, "pl": 0.05},
    "off-ball screen": {"hr_change": 1, "speed": 0.8, "accel": 0.3, "pl": 0.03},
    "help defense": {"hr_change": 3, "speed": 4.0, "accel": 2.0, "pl": 0.15},
    "contest": {"hr_change": 2, "speed": 2.0, "accel": 1.0, "pl": 0.1},
    "rebound": {"hr_change": 4, "speed": 3.0, "accel": 3.0, "pl": 0.2},
    "box out": {"hr_change": 1, "speed": 0.5, "accel": 0.5, "pl": 0.05},
    "pass": {"hr_change": 2, "speed": 3.0, "accel": 1.5, "pl": 0.1},
    "catch": {"hr_change": 1, "speed": 0.5, "accel": 0.2, "pl": 0.02},
    "shot": {"hr_change": 3, "speed": 0.0, "accel": 2.0, "pl": 0.1},
    "offensive rebound": {"hr_change": 4, "speed": 3.0, "accel": 3.0, "pl": 0.2},
    "defensive rebound": {"hr_change": 4, "speed": 3.0, "accel": 3.0, "pl": 0.2},
    "flare screen": {"hr_change": 1, "speed": 0.8, "accel": 0.3, "pl": 0.03},
    "pop screen": {"hr_change": 1, "speed": 0.8, "accel": 0.3, "pl": 0.03},
    "backdoor cut": {"hr_change": 4, "speed": 5.5, "accel": 2.5, "pl": 0.2},
    "relocate": {"hr_change": 2, "speed": 3.0, "accel": 0.5, "pl": 0.05},
    "sliding": {"hr_change": 2, "speed": 2.0, "accel": 1.2, "pl": 0.1},
    "over screen": {"hr_change": 3, "speed": 4.0, "accel": 2.5, "pl": 0.15},
    "drop coverage": {"hr_change": 1, "speed": 1.0, "accel": 0.5, "pl": 0.05},
    "chase": {"hr_change": 5, "speed": 6.5, "accel": 3.5, "pl": 0.3},
    "recover": {"hr_change": 2, "speed": 3.5, "accel": 1.5, "pl": 0.1},
    "fight rebound": {"hr_change": 4, "speed": 3.0, "accel": 3.0, "pl": 0.2},
    "ball pressure": {"hr_change": 3, "speed": 2.5, "accel": 1.8, "pl": 0.12},
    "move to screen": {"hr_change": 2, "speed": 2.5, "accel": 1.0, "pl": 0.08},
    "pop": {"hr_change": 2, "speed": 2.0, "accel": 1.0, "pl": 0.1},
    "rebound position": {"hr_change": 1, "speed": 1.0, "accel": 0.5, "pl": 0.05},
    "slide": {"hr_change": 2, "speed": 2.0, "accel": 1.2, "pl": 0.1},
    "lost man": {"hr_change": 4, "speed": 4.5, "accel": 2.8, "pl": 0.22},
    "switch": {"hr_change": 3, "speed": 3.5, "accel": 2.0, "pl": 0.15},
    "possession over": {"hr_change": -2, "speed": 0.0, "accel": 0.0, "pl": 0.0}
}

# Default moderate intensity for unknown actions
DEFAULT_INTENSITY = {"hr_change": 2, "speed": 2.0, "accel": 1.0, "pl": 0.1}

def generate_biometrics(possession_df):
    times = np.arange(0, 24.1, 0.5)  # 0.5s intervals (0.0 to 24.0)
    player_data = []
    np.random.seed(42)  # For reproducibility
    
    # Individual baseline HR for each player
    base_hr = 90
    hr_variation = {player: np.random.randint(-5, 6) for player in possession_df['player'].unique()}
    
    for player in possession_df['player'].unique():
        hr = base_hr + hr_variation[player]
        pl_total = 0.0  # Cumulative PlayerLoad
        
        for t in times:
            # Get nearest second action (floor the time)
            second = int(np.floor(t))
            action_row = possession_df[
                (possession_df['time'] == second) & 
                (possession_df['player'] == player)
            ]
            
            if not action_row.empty:
                action = action_row['action'].values[0]
                x = action_row['x'].values[0]
                y = action_row['y'].values[0]
                
                # Get intensity profile or use default
                intensity = ACTION_INTENSITY.get(action, DEFAULT_INTENSITY)
                
                # Update heart rate with random variation
                hr_change = intensity["hr_change"] + np.random.uniform(-1.5, 1.5)
                hr += hr_change
                hr = np.clip(hr, 50, 190)  # Keep within physiological range
                
                # Calculate velocity and acceleration with randomness
                speed = intensity["speed"] * np.random.uniform(0.5, 1.5)
                accel = intensity["accel"] * np.random.uniform(0.5, 1.5)
                
                # Update PlayerLoad with randomness
                pl_increment = intensity["pl"] * np.random.uniform(0.8, 1.2)
                pl_total += pl_increment
                
                # Add physiological lag effect
                if t > 0 and t % 1 == 0.5:  # At half-second marks
                    hr = hr * 0.99  # Slight decay if no new stimulus
                
                player_data.append({
                    'time': round(t, 1),
                    'player': player,
                    'x': x,
                    'y': y,
                    'action': action,
                    'heart_rate': int(hr),
                    'velocity': round(speed, 2),
                    'acceleration': round(accel, 2),
                    'player_load': round(pl_total, 2)
                })
    
    return pd.DataFrame(player_data)

if __name__ == "__main__":
    print("Simulating possession data...")
    possession = simulate_possession()
    print("Generating biometric data...")
    biometrics = generate_biometrics(possession)
    
    # Save to CSV with appropriate precision
    biometrics.to_csv('../data/biometric_data.csv', index=False, float_format='%.2f')
    print(f"Biometric data saved to data/biometric_data.csv")
    print(f"Generated {len(biometrics)} records at 0.5s intervals")
    
    # Print sample output matching PDF example
    print("\nSample output (first 10 rows for A1):")
    sample = biometrics[
        (biometrics['player'] == 'A1') & 
        (biometrics['time'] <= 4.5)
    ].head(10)
    print(sample[['time', 'player', 'action', 'x', 'y', 'heart_rate', 
                  'velocity', 'acceleration', 'player_load']])