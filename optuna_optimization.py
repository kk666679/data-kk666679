# optuna_optimization.py
import optuna
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC
import xgboost as xgb
import lightgbm as lgb
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import warnings
warnings.filterwarnings('ignore')

# Load dataset
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def objective_random_forest(trial):
    """Optimize Random Forest hyperparameters"""
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
        'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy'])
    }
    
    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return f1_score(y_test, preds)

def objective_svm(trial):
    """Optimize SVM hyperparameters"""
    params = {
        'C': trial.suggest_float('C', 1e-3, 1e3, log=True),
        'gamma': trial.suggest_float('gamma', 1e-3, 1e3, log=True),
        'kernel': trial.suggest_categorical('kernel', ['linear', 'rbf', 'poly']),
        'degree': trial.suggest_int('degree', 2, 5)  # Only used for poly kernel
    }
    
    model = SVC(**params, probability=True)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)

def objective_xgboost(trial):
    """Optimize XGBoost hyperparameters"""
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
        'lambda': trial.suggest_float('lambda', 1e-3, 10.0, log=True),
        'alpha': trial.suggest_float('alpha', 1e-3, 10.0, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'eta': trial.suggest_float('eta', 1e-3, 1.0, log=True),
        'gamma': trial.suggest_float('gamma', 1e-3, 1.0, log=True),
        'grow_policy': trial.suggest_categorical('grow_policy', ['depthwise', 'lossguide'])
    }
    
    if params['booster'] == 'gbtree' or params['booster'] == 'dart':
        params['subsample'] = trial.suggest_float('subsample', 0.5, 1.0)
        params['colsample_bytree'] = trial.suggest_float('colsample_bytree', 0.5, 1.0)
    
    model = xgb.XGBClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return f1_score(y_test, preds)

def objective_lightgbm(trial):
    """Optimize LightGBM hyperparameters"""
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'boosting_type': trial.suggest_categorical('boosting_type', ['gbdt', 'dart', 'goss']),
        'num_leaves': trial.suggest_int('num_leaves', 10, 100),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.1, log=True),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True)
    }
    
    model = lgb.LGBMClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return f1_score(y_test, preds)

class SimpleNN(nn.Module):
    """Simple neural network for PyTorch optimization"""
    def __init__(self, input_dim, hidden_dim, dropout_rate):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return self.sigmoid(x)

def objective_pytorch(trial):
    """Optimize PyTorch neural network hyperparameters"""
    # Convert data to PyTorch tensors
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train).reshape(-1, 1)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test).reshape(-1, 1)
    
    # Create dataset and dataloader
    train_dataset = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    # Suggest hyperparameters
    params = {
        'hidden_dim': trial.suggest_int('hidden_dim', 16, 128),
        'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5),
        'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
        'weight_decay': trial.suggest_float('weight_decay', 1e-5, 1e-3, log=True)
    }
    
    # Initialize model
    model = SimpleNN(X_train.shape[1], params['hidden_dim'], params['dropout_rate'])
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), 
                         lr=params['learning_rate'],
                         weight_decay=params['weight_decay'])
    
    # Training loop
    for epoch in range(50):  # Fixed number of epochs for demo
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
    
    # Evaluation
    with torch.no_grad():
        outputs = model(X_test_t)
        preds = (outputs > 0.5).float()
        accuracy = (preds == y_test_t).float().mean()
    
    return accuracy.item()

def run_optimization(objective, n_trials=50, study_name=None):
    """Run Optuna optimization for a given objective"""
    study = optuna.create_study(
        direction='maximize',
        study_name=study_name,
        sampler=optuna.samplers.TPESampler(),
        pruner=optuna.pruners.HyperbandPruner()
    )
    
    study.optimize(objective, n_trials=n_trials)
    
    print(f"\nBest trial for {study_name}:")
    trial = study.best_trial
    print(f"  Value: {trial.value:.4f}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
    
    return study

def main():
    # Run optimizations for different models
    print("=== Running Hyperparameter Optimization ===")
    
    print("\n1. Random Forest Optimization")
    rf_study = run_optimization(objective_random_forest, n_trials=30, study_name="RandomForest")
    
    print("\n2. SVM Optimization")
    svm_study = run_optimization(objective_svm, n_trials=30, study_name="SVM")
    
    print("\n3. XGBoost Optimization")
    xgb_study = run_optimization(objective_xgboost, n_trials=30, study_name="XGBoost")
    
    print("\n4. LightGBM Optimization")
    lgbm_study = run_optimization(objective_lightgbm, n_trials=30, study_name="LightGBM")
    
    print("\n5. PyTorch Neural Network Optimization")
    torch_study = run_optimization(objective_pytorch, n_trials=20, study_name="PyTorchNN")
    
    # Visualize results
    try:
        import optuna.visualization as vis
        fig = vis.plot_optimization_history(rf_study)
        fig.show()
    except ImportError:
        print("\nInstall plotly for visualization: pip install plotly")

if __name__ == "__main__":
    main()
