import pandas as pd

def read_top_three():
    """Function that grabs the top three scores and returns them as a dict"""
    
    # try to read csv if exists
    try:
        df = pd.read_csv("scores.csv", names=["score", "medal"])
        df = df.sort_values("score", ascending=False)
        data = df.head(3).to_dict('records')
        # print(df.head(3))
        # print(data)
        if len(data) == 0:
            return "No scores found"
        return data
    except:
        return "No scores found"


def log_score(score, medal):
    """Function that takes the score and medal type and places it in the csv"""
    
    # make a new dict
    data = {"score": [score], "medal": [medal]}

    # make a df from data
    df = pd.DataFrame(data)

    # try to append/write to scores.csv
    try:
        df.to_csv('scores.csv', mode='a', index=False, header=False)
        print(f"Successfully logged {score} and {medal} to csv")
    except:
        print("Failed to write")