import numpy as np
import pandas as pd

def simulate_possession():
    # Court dimensions (FIBA standard)
    COURT_LENGTH = 28
    COURT_WIDTH = 15
    
    # Player positions and actions per second (0-24s)
    timeline = {
        # t=0s
        0: {
            'A1': {'x': 21.0, 'y': 7.5, 'action': 'ball hold'},
            'A2': {'x': 20.0, 'y': 11.0, 'action': 'static'},
            'A3': {'x': 20.0, 'y': 4.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 5.0, 'action': 'static'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 20.0, 'y': 7.5, 'action': 'ball pressure'},
            'D2': {'x': 19.5, 'y': 11.0, 'action': 'static'},
            'D3': {'x': 19.5, 'y': 4.0, 'action': 'static'},
            'D4': {'x': 22.5, 'y': 5.0, 'action': 'static'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=1s
        1: {
            'A1': {'x': 21.0, 'y': 7.5, 'action': 'ball hold'},
            'A2': {'x': 20.0, 'y': 11.0, 'action': 'static'},
            'A3': {'x': 20.0, 'y': 4.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 5.0, 'action': 'static'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 20.0, 'y': 7.5, 'action': 'ball pressure'},
            'D2': {'x': 19.5, 'y': 11.0, 'action': 'static'},
            'D3': {'x': 19.5, 'y': 4.0, 'action': 'static'},
            'D4': {'x': 22.5, 'y': 5.0, 'action': 'static'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=2s
        2: {
            'A1': {'x': 21.0, 'y': 7.5, 'action': 'ball hold'},
            'A2': {'x': 20.0, 'y': 11.0, 'action': 'static'},
            'A3': {'x': 20.0, 'y': 4.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 5.0, 'action': 'static'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 20.0, 'y': 7.5, 'action': 'ball pressure'},
            'D2': {'x': 19.5, 'y': 11.0, 'action': 'static'},
            'D3': {'x': 19.5, 'y': 4.0, 'action': 'static'},
            'D4': {'x': 22.5, 'y': 5.0, 'action': 'static'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=3s
        3: {
            'A1': {'x': 20.5, 'y': 7.0, 'action': 'pass'},
            'A2': {'x': 22.0, 'y': 13.0, 'action': 'cut'},
            'A3': {'x': 20.0, 'y': 4.0, 'action': 'catch'},
            'A4': {'x': 21.0, 'y': 6.5, 'action': 'flare screen'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 19.5, 'y': 7.0, 'action': 'ball pressure'},
            'D2': {'x': 21.0, 'y': 12.0, 'action': 'sliding'},
            'D3': {'x': 19.5, 'y': 4.0, 'action': 'static'},
            'D4': {'x': 22.0, 'y': 6.0, 'action': 'drop coverage'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=4s
        4: {
            'A1': {'x': 19.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 25.0, 'y': 14.0, 'action': 'cut'},
            'A3': {'x': 19.0, 'y': 4.0, 'action': 'dribble'},
            'A4': {'x': 21.0, 'y': 6.5, 'action': 'flare screen'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 18.0, 'y': 7.0, 'action': 'sliding'},
            'D2': {'x': 24.0, 'y': 13.5, 'action': 'sliding'},
            'D3': {'x': 18.5, 'y': 4.2, 'action': 'ball pressure'},
            'D4': {'x': 22.0, 'y': 6.0, 'action': 'drop coverage'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=5s
        5: {
            'A1': {'x': 17.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'A3': {'x': 18.0, 'y': 4.0, 'action': 'static'},
            'A4': {'x': 21.0, 'y': 6.5, 'action': 'static'},
            'A5': {'x': 23.0, 'y': 10.0, 'action': 'static'},
            'D1': {'x': 16.5, 'y': 7.0, 'action': 'sliding'},
            'D2': {'x': 27.0, 'y': 14.5, 'action': 'sliding'},
            'D3': {'x': 17.5, 'y': 4.0, 'action': 'ball pressure'},
            'D4': {'x': 22.0, 'y': 6.0, 'action': 'drop coverage'},
            'D5': {'x': 22.5, 'y': 10.0, 'action': 'static'}
        },
        # t=6s
        6: {
            'A1': {'x': 18.0, 'y': 7.5, 'action': 'catch'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'A3': {'x': 15.0, 'y': 4.0, 'action': 'pass'},
            'A4': {'x': 19.0, 'y': 7.5, 'action': 'move to screen'},
            'A5': {'x': 23.0, 'y': 9.0, 'action': 'static'},
            'D1': {'x': 17.0, 'y': 7.5, 'action': 'ball pressure'},
            'D2': {'x': 27.0, 'y': 14.5, 'action': 'static'},
            'D3': {'x': 14.0, 'y': 4.5, 'action': 'sliding'},
            'D4': {'x': 18.0, 'y': 7.0, 'action': 'static'},
            'D5': {'x': 22.5, 'y': 9.5, 'action': 'static'}
        },
        # t=7s
        7: {
            'A1': {'x': 18.0, 'y': 7.0, 'action': 'dribble'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'relocate'},
            'A3': {'x': 15.0, 'y': 7.0, 'action': 'relocate'},
            'A4': {'x': 18.0, 'y': 7.5, 'action': 'on-ball screen'},
            'A5': {'x': 23.0, 'y': 8.0, 'action': 'static'},
            'D1': {'x': 17.5, 'y': 7.5, 'action': 'over screen'},
            'D2': {'x': 25.0, 'y': 13.0, 'action': 'sliding'},
            'D3': {'x': 14.5, 'y': 7.0, 'action': 'sliding'},
            'D4': {'x': 18.5, 'y': 6.5, 'action': 'drop coverage'},
            'D5': {'x': 22.0, 'y': 8.5, 'action': 'static'}
        },
        # t=8s
        8: {
            'A1': {'x': 20.0, 'y': 9.0, 'action': 'dribble'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'static'},
            'A3': {'x': 15.0, 'y': 3.0, 'action': 'static'},
            'A4': {'x': 20.0, 'y': 6.0, 'action': 'roll'},
            'A5': {'x': 23.0, 'y': 7.0, 'action': 'static'},
            'D1': {'x': 19.0, 'y': 8.5, 'action': 'chase'},
            'D2': {'x': 26.0, 'y': 12.5, 'action': 'static'},
            'D3': {'x': 15.5, 'y': 3.5, 'action': 'static'},
            'D4': {'x': 19.5, 'y': 5.5, 'action': 'drop coverage'},
            'D5': {'x': 21.0, 'y': 7.0, 'action': 'help defense'}
        },
        # t=9s
        9: {
            'A1': {'x': 22.0, 'y': 9.5, 'action': 'dribble'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'static'},
            'A3': {'x': 15.0, 'y': 3.0, 'action': 'static'},
            'A4': {'x': 21.5, 'y': 4.0, 'action': 'roll'},
            'A5': {'x': 23.0, 'y': 6.0, 'action': 'static'},
            'D1': {'x': 21.0, 'y': 9.0, 'action': 'chase'},
            'D2': {'x': 26.0, 'y': 12.5, 'action': 'static'},
            'D3': {'x': 15.5, 'y': 3.5, 'action': 'static'},
            'D4': {'x': 20.0, 'y': 5.0, 'action': 'drop coverage'},
            'D5': {'x': 20.5, 'y': 5.0, 'action': 'help defense'}
        },
        # t=10s
        10: {
            'A1': {'x': 22.0, 'y': 9.5, 'action': 'pass'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'static'},
            'A3': {'x': 15.0, 'y': 3.0, 'action': 'static'},
            'A4': {'x': 21.5, 'y': 4.0, 'action': 'catch'},
            'A5': {'x': 23.0, 'y': 5.0, 'action': 'static'},
            'D1': {'x': 22.0, 'y': 8.5, 'action': 'recover'},
            'D2': {'x': 26.0, 'y': 12.5, 'action': 'static'},
            'D3': {'x': 15.5, 'y': 3.5, 'action': 'static'},
            'D4': {'x': 20.5, 'y': 4.5, 'action': 'contest'},
            'D5': {'x': 20.5, 'y': 4.0, 'action': 'contest'}
        },
        # t=11s
        11: {
            'A1': {'x': 22.0, 'y': 8.0, 'action': 'static'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'static'},
            'A3': {'x': 15.0, 'y': 3.0, 'action': 'static'},
            'A4': {'x': 19.0, 'y': 6.0, 'action': 'pop'},
            'A5': {'x': 23.0, 'y': 4.0, 'action': 'rebound position'},
            'D1': {'x': 21.0, 'y': 7.0, 'action': 'help defense'},
            'D2': {'x': 26.0, 'y': 12.5, 'action': 'static'},
            'D3': {'x': 15.5, 'y': 3.5, 'action': 'static'},
            'D4': {'x': 19.5, 'y': 5.5, 'action': 'slide'},
            'D5': {'x': 19.5, 'y': 5.0, 'action': 'contest'}
        },
        # t=12s
        12: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 26.0, 'y': 13.0, 'action': 'static'},
            'A3': {'x': 18.0, 'y': 1.0, 'action': 'backdoor cut'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'pop screen'},
            'A5': {'x': 23.0, 'y': 3.5, 'action': 'static'},
            'D1': {'x': 20.0, 'y': 6.5, 'action': 'help defense'},
            'D2': {'x': 26.0, 'y': 12.5, 'action': 'static'},
            'D3': {'x': 17.0, 'y': 2.0, 'action': 'lost man'},
            'D4': {'x': 23.0, 'y': 7.0, 'action': 'switch'},
            'D5': {'x': 22.5, 'y': 4.0, 'action': 'recover'}
        },
        # t=13s
        13: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'A3': {'x': 19.0, 'y': 2.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'pass'},
            'A5': {'x': 23.0, 'y': 3.0, 'action': 'static'},
            'D1': {'x': 19.0, 'y': 6.5, 'action': 'static'},
            'D2': {'x': 27.0, 'y': 14.0, 'action': 'sliding'},
            'D3': {'x': 18.5, 'y': 2.5, 'action': 'recover'},
            'D4': {'x': 23.0, 'y': 7.5, 'action': 'ball pressure'},
            'D5': {'x': 22.5, 'y': 3.5, 'action': 'static'}
        },
        # t=14s
        14: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'catch'},
            'A3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'static'},
            'A5': {'x': 23.0, 'y': 2.5, 'action': 'static'},
            'D1': {'x': 18.0, 'y': 7.0, 'action': 'static'},
            'D2': {'x': 28.0, 'y': 14.5, 'action': 'contest'},
            'D3': {'x': 19.5, 'y': 2.5, 'action': 'static'},
            'D4': {'x': 23.0, 'y': 7.5, 'action': 'static'},
            'D5': {'x': 22.0, 'y': 2.5, 'action': 'box out'}
        },
        # t=15s
        15: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'shot'},
            'A3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'static'},
            'A5': {'x': 24.0, 'y': 2.0, 'action': 'offensive rebound'},
            'D1': {'x': 20.0, 'y': 5.0, 'action': 'box out'},
            'D2': {'x': 28.0, 'y': 15.0, 'action': 'contest'},
            'D3': {'x': 20.0, 'y': 2.0, 'action': 'box out'},
            'D4': {'x': 22.0, 'y': 7.0, 'action': 'box out'},
            'D5': {'x': 23.0, 'y': 2.0, 'action': 'box out'}
        },
        # t=16s (rebound - possession ends)
        16: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'static'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'A3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'static'},
            'A5': {'x': 24.0, 'y': 1.5, 'action': 'fight rebound'},
            'D1': {'x': 20.0, 'y': 5.0, 'action': 'static'},
            'D2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'D3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'D4': {'x': 22.0, 'y': 7.0, 'action': 'static'},
            'D5': {'x': 23.0, 'y': 1.5, 'action': 'defensive rebound'}
        },
        # t=17s (possession over)
        17: {
            'A1': {'x': 20.0, 'y': 7.0, 'action': 'possession over'},
            'A2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'A3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'A4': {'x': 23.0, 'y': 7.5, 'action': 'static'},
            'A5': {'x': 24.0, 'y': 1.5, 'action': 'static'},
            'D1': {'x': 20.0, 'y': 5.0, 'action': 'static'},
            'D2': {'x': 28.0, 'y': 15.0, 'action': 'static'},
            'D3': {'x': 20.0, 'y': 2.0, 'action': 'static'},
            'D4': {'x': 22.0, 'y': 7.0, 'action': 'static'},
            'D5': {'x': 23.0, 'y': 1.5, 'action': 'static'}
        },
        # t=18s to 24s (static/reset)
        #18: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #19: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #20: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #21: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #22: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #23: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()},
        #24: {k: {**v, 'action': 'static'} for k, v in timeline[17].items()}
    }
    
    # Convert to DataFrame
    data = []
    for t, players in timeline.items():
        for player, info in players.items():
            data.append({
                'time': t,
                'player': player,
                'x': info['x'],
                'y': info['y'],
                'action': info['action']
            })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = simulate_possession()
    # Save to CSV with float precision
    df.to_csv('../data/simulated_possession.csv', index=False, float_format='%.1f')
    print("Simulated possession data saved to data/simulated_possession.csv")