"""Hyperparameter tuning using Optuna.

Provides framework for tuning alpha strategy parameters using Optuna optimization.
"""

import optuna
from typing import Dict, Any, Callable
from pathlib import Path
import json


class AlphaHPT:
    """Hyperparameter tuning for alpha strategies."""

    def __init__(self, alpha_class: type, backtest_func: Callable, config: Dict[str, Any]):
        """
        Initialize HPT framework.

        Args:
            alpha_class: Alpha class to tune
            backtest_func: Function to run backtest and return PnL/sharpe
            config: Configuration including parameter ranges
        """
        self.alpha_class = alpha_class
        self.backtest_func = backtest_func
        self.config = config
        self.study = None

    def create_objective(self, param_space: Dict[str, Any]) -> Callable:
        """
        Create objective function for Optuna.

        Args:
            param_space: Dictionary defining parameter ranges
                e.g., {'z_lookback': ('int', 10, 200),
                       'threshold': ('float', 1.0, 3.0)}

        Returns:
            Objective function for Optuna to optimize
        """
        def objective(trial: optuna.Trial) -> float:
            # Suggest parameters based on param_space
            params = {}
            for param_name, param_config in param_space.items():
                param_type = param_config[0]
                if param_type == 'int':
                    params[param_name] = trial.suggest_int(
                        param_name, param_config[1], param_config[2]
                    )
                elif param_type == 'float':
                    params[param_name] = trial.suggest_float(
                        param_name, param_config[1], param_config[2]
                    )
                elif param_type == 'categorical':
                    params[param_name] = trial.suggest_categorical(
                        param_name, param_config[1]
                    )

            # Run backtest with these parameters
            pnl = self.backtest_func(self.alpha_class, params)
            return pnl

        return objective

    def run_optimization(self, param_space: Dict[str, Any], n_trials: int = 100) -> Dict[str, Any]:
        """
        Run hyperparameter optimization.

        Args:
            param_space: Parameter space definition
            n_trials: Number of optimization trials

        Returns:
            Dictionary with best parameters and study results
        """
        objective = self.create_objective(param_space)

        self.study = optuna.create_study(direction='maximize')
        self.study.optimize(objective, n_trials=n_trials)

        results = {
            'best_params': self.study.best_params,
            'best_value': self.study.best_value,
            'n_trials': len(self.study.trials),
        }
        return results

    def save_study(self, output_path: Path) -> None:
        """
        Save Optuna study to file.

        Args:
            output_path: Path to save study results
        """
        if self.study is None:
            raise ValueError("No study to save. Run optimization first.")

        study_data = {
            'best_params': self.study.best_params,
            'best_value': self.study.best_value,
            'trials': [
                {
                    'number': trial.number,
                    'value': trial.value,
                    'params': trial.params,
                }
                for trial in self.study.trials
            ],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(study_data, f, indent=2)


def example_pairs_hpt():
    """
    Example HPT for AlphaPairs strategy.

    This demonstrates how to tune the z-score lookback and threshold parameters.
    """
    # Define parameter space
    param_space = {
        'z_lookback': ('int', 10, 200),
        'entry_threshold': ('float', 1.5, 3.0),
        'exit_threshold': ('float', 0.3, 1.0),
    }

    # Example backtest function (placeholder)
    def backtest_function(alpha_class, params):
        # TODO: Run actual backtest
        # For now, return dummy PnL
        return 100.0

    # Run HPT
    from src.alphas.alpha_pairs import AlphaPairs
    hpt = AlphaHPT(AlphaPairs, backtest_function, {})
    results = hpt.run_optimization(param_space, n_trials=50)

    print(f"Best parameters: {results['best_params']}")
    print(f"Best PnL: {results['best_value']}")

    # Save results
    hpt.save_study(Path('results/hpt/alpha_pairs_hpt.json'))


if __name__ == '__main__':
    example_pairs_hpt()
