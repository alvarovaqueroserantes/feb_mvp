import pandas as pd
import numpy as np

def integrate_datasets():
    # Load simulated data
    possession = pd.read_csv('../data/simulated_possession.csv')
    biometrics = pd.read_csv('../data/biometric_data.csv')
    
    # Merge datasets - biometrics already contains position and action data
    # We'll keep the biometrics as primary since it has higher time resolution
    merged = biometrics.copy()
    
    # Add court zones based on FIBA court dimensions (28m x 15m)
    # Court zone definitions:
    # 1. Backcourt: Offensive half (x < 14m)
    # 2. Frontcourt: Defensive half (x >= 14m)
    # 3. Paint/Key: The rectangular area near the basket
    # 4. Perimeter: Areas beyond the paint but inside three-point line
    # 5. Corners: The corner three-point areas
    # 6. Top of Key: Area around the top of the three-point arc
    # 7. Wings: Areas along the sides of the court
    # 8. Dunker Spot: Specific low post positions
    
    # FIBA court dimensions reference:
    # - Paint: 4.9m wide (from y=5.3 to y=9.7 at center y=7.5)
    # - Three-point line: 6.75m from basket at top, 6.6m in corners
    # - Basket located at (28, 7.5)
    
    # Define court zones
    merged['zone'] = np.select(
        [
            # Backcourt (offensive half)
            (merged['x'] < 14),
            
            # Frontcourt areas
            # Paint/Key area (rectangular)
            (merged['x'] >= 22) & (merged['x'] <= 28) & 
            (merged['y'] >= 5.3) & (merged['y'] <= 9.7),
            
            # Left Corner (three-point area)
            (merged['x'] >= 22) & (merged['y'] < 5.3),
            
            # Right Corner (three-point area)
            (merged['x'] >= 22) & (merged['y'] > 9.7),
            
            # Top of Key (around three-point arc)
            (merged['x'] >= 18) & (merged['x'] < 22) & 
            (merged['y'] >= 6.0) & (merged['y'] <= 9.0),
            
            # Left Wing
            (merged['x'] >= 14) & (merged['x'] < 22) & 
            (merged['y'] < 7.5) & (merged['y'] >= 3.0),
            
            # Right Wing
            (merged['x'] >= 14) & (merged['x'] < 22) & 
            (merged['y'] > 7.5) & (merged['y'] <= 12.0),
            
            # Dunker Spot (left)
            (merged['x'] >= 25) & (merged['x'] <= 28) & 
            (merged['y'] >= 3.0) & (merged['y'] < 5.3),
            
            # Dunker Spot (right)
            (merged['x'] >= 25) & (merged['x'] <= 28) & 
            (merged['y'] > 9.7) & (merged['y'] <= 12.0),
            
            # High Post (free throw line area)
            (merged['x'] >= 20) & (merged['x'] < 22) & 
            (merged['y'] >= 5.3) & (merged['y'] <= 9.7),
            
            # Mid-range areas
            (merged['x'] >= 14) & (merged['x'] < 18) & 
            (merged['y'] >= 5.0) & (merged['y'] <= 10.0),
        ],
        [
            'backcourt',
            'paint',
            'left_corner',
            'right_corner',
            'top_key',
            'left_wing',
            'right_wing',
            'dunker_left',
            'dunker_right',
            'high_post',
            'mid_range'
        ],
        default='other_frontcourt'
    )
    
    # Add additional tactical features
    # 1. Distance to basket
    basket_x, basket_y = 28.0, 7.5
    merged['dist_to_basket'] = np.sqrt(
        (merged['x'] - basket_x)**2 + 
        (merged['y'] - basket_y)**2
    )
    
    # 2. Player role based on position
    merged['role'] = np.select(
        [
            merged['player'].str.startswith('A1') | merged['player'].str.startswith('D1'),
            merged['player'].str.startswith('A2') | merged['player'].str.startswith('A3') |
            merged['player'].str.startswith('D2') | merged['player'].str.startswith('D3'),
            merged['player'].str.startswith('A4') | merged['player'].str.startswith('A5') |
            merged['player'].str.startswith('D4') | merged['player'].str.startswith('D5'),
        ],
        [
            'guard',
            'wing',
            'big'
        ],
        default='unknown'
    )
    
    # 3. Action type categories
    merged['action_type'] = np.select(
        [
            merged['action'].isin(['cut', 'sprint', 'drive', 'roll', 'backdoor cut']),
            merged['action'].isin(['dribble', 'relocate', 'sliding', 'chase', 'recover']),
            merged['action'].isin(['ball hold', 'static', 'jog', 'walk', 'possession over'])
        ],
        [
            'high_intensity',
            'medium_intensity',
            'low_intensity'
        ],
        default='special_action'
    )
    
    # Save integrated dataset
    merged.to_csv('../data/integrated_dataset.csv', index=False, float_format='%.2f')
    return merged

if __name__ == "__main__":
    print("Integrating datasets...")
    integrated_data = integrate_datasets()
    print(f"Integrated dataset saved to data/integrated_dataset.csv")
    print(f"Total records: {len(integrated_data)}")
    print("\nSample of integrated data:")
    print(integrated_data[['time', 'player', 'action', 'zone', 'heart_rate', 'player_load']].head(10))