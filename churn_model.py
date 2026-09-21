# Projeto Churn - script reproduzível
# Consulte README.md para as perguntas e conclusões de negócio.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("Churn_Modelling.csv")
X = df.drop(columns=["Exited", "RowNumber", "CustomerId", "Surname"])
y = df["Exited"]
cat = ["Geography", "Gender"]
num = [c for c in X.columns if c not in cat]
preprocess = ColumnTransformer([(
    "num", StandardScaler(), num),
    ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), cat),
])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model = Pipeline([(
    "preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=500, max_depth=8, min_samples_leaf=8, class_weight="balanced", random_state=42, n_jobs=-1)),
])
model.fit(X_train, y_train)
probabilidade_churn = model.predict_proba(X_test)[:, 1]
