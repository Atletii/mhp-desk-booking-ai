import pickle
import re

import pandas as pd
import sklearn

def feature_eng_room(df):
    df_pop = pd.read_csv('room_day_pop.csv')

    df_prox = pd.DataFrame({
        'room': ['Pit-Lane', 'Dry-lane', 'Joker Lap', 'Quick 8', 'Pole Position', 'Cockpit'],
        'proximity': [1.3, 1.3, 2, 10, 25, 35]
    })

    df = df.merge(df_prox, on=['room'])

    df_id = pd.DataFrame({
        'room': ['Pit-Lane', 'Dry-lane', 'Joker Lap', 'Quick 8', 'Pole Position', 'Cockpit'],
        'new': [0, 1, 2, 3, 4, 5]
    })

    df = df.merge(df_id, on=['room'])
    df['room'] = df['new']

    df = df.drop(columns=['new'])

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek

    df = df.merge(df_pop, on=['day_of_week', 'room'])

    df = df.drop(columns=['date'])

    return df


def predict_room(room, date, timeframe):
    if timeframe not in ['nineToEleven', 'elevenToOne', 'oneToThree', 'threeToFive']:
        raise ValueError("Parameter 'timeframe' must be in ['nineToEleven', 'elevenToOne', 'oneToThree', "
                         "'threeToFive'].")
    if room not in ['Pit-Lane', 'Dry-lane', 'Joker Lap', 'Quick 8', 'Pole Position', 'Cockpit']:
        raise ValueError("Parameter 'room' must be in ['Pit-Lane', 'Dry-lane', 'Joker Lap', 'Quick 8', "
                         "'Pole Position', 'Cockpit'].")

    df = pd.DataFrame({'room': [room],
                       'date': [date]})

    df = feature_eng_room(df)

    if df.empty:
        raise ValueError("Something went wrong")

    if timeframe == 'nineToEleven':
        model = pickle.load(open('room_9_11_pred.pk1', 'rb'))
    elif timeframe == 'elevenToOne':
        model = pickle.load(open('room_11_1_pred.pk1', 'rb'))
    elif timeframe == 'oneToThree':
        model = pickle.load(open('room_1_3_pred.pk1', 'rb'))
    else:
        model = pickle.load(open('room_3_5_pred.pk1', 'rb'))

    pred = model.predict_proba(df)[:, 1][0]
    print(pred)
    return pred


def predict_desk(desk, date, half):
    if half not in ['first', 'second']:
        raise ValueError("Parameter 'half' must be either 'first' or 'second'.")

    df = pd.DataFrame({'desk': [desk],
                       'date': [date]})

    df = feature_eng_desk(df)

    if df.empty:
        raise ValueError("Desk ID not valid")

    print(df)

    if half == 'first':
        model = pickle.load(open('desk_first_pred.pk1', 'rb'))

    else:
        model = pickle.load(open('desk_second_pred.pk1', 'rb'))

    pred = model.predict_proba(df)[:, 1][0]
    print(pred)
    return pred


def feature_eng_desk(df):
    df_pop = pd.read_csv('desk_day_pop.csv')

    df['ID'] = df['desk'].apply(generate_id)

    df['proximity'] = df['desk'].apply(proximity_to_exit)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek

    df = df.drop(columns=['desk', 'date'])

    df = df.merge(df_pop, on=['day_of_week', 'ID'])

    return df


def generate_id(desk):
    match = re.match(r'([A-Z]+)_([0-9]+)_([a-zA-Z]+)_([0-9]+).([0-9]+)', desk)
    if match:
        return int(match.group(2)) * 1000000 + int(match.group(4)) * 1000 + int(match.group(5))
    else:
        return None


def proximity_to_exit(desk):
    match = re.match(r'([A-Z]+)_([0-9]+)_([a-zA-Z]+)_([0-9]+).([0-9]+)', desk)
    if match:
        return int(match.group(4)) + int(match.group(5))
    else:
        return None


# predict_desk('CLUJ_5_beta_5.3', '25/03/2024', 'second')
#
# predict_room('Joker Lap', '1/4/2024', 'elevenToOne')