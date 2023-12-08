import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib
from prepare_dataset import prepare_data


df = prepare_data('../UCI_Credit_Card.csv')

X = df.drop('default', axis=1)
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

oversample = SMOTE()
X_train, y_train = oversample.fit_resample(X_train, y_train)
params = {'max_depth': 11,
          'min_samples_leaf': 1,
          'min_samples_split': 2,
          'n_estimators': 300}

model = RandomForestClassifier(**params)
model.fit(X_train, y_train)
joblib.dump(model, 'model.pkl')
