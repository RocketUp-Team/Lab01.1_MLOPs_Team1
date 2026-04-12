"""
Script to train and save the movie rating prediction model.

This script:
1. Loads the MovieLens 100K dataset (via Surprise built-in downloader)
2. Trains an SVD model using collaborative filtering (matrix factorization)
3. (Optional) Evaluates the model with cross-validation
4. Saves the trained model to disk

Usage:
    python scripts/train_model.py
"""

import pickle
from pathlib import Path

from surprise import Dataset, SVD
from surprise.model_selection import cross_validate


def main() -> None:
    print("=" * 60)
    print("Movie Rating Prediction Model Training (Surprise SVD)")
    print("=" * 60)

    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / "svd_model.pkl"

    # ----------------------------------------------------------------------
    # Step 1: Load data
    # ----------------------------------------------------------------------
    print("\n[1/4] Loading MovieLens 100K dataset (ml-100k)...")
    data = Dataset.load_builtin("ml-100k")
    print("      Dataset loaded successfully!")

    # ----------------------------------------------------------------------
    # Step 2: Cross-validation (kept for assignment completeness)
    # ----------------------------------------------------------------------
    print("\n[2/4] Performing cross-validation...")
    algo = SVD(
        n_factors=100,
        n_epochs=20,
        lr_all=0.005,
        reg_all=0.02,
        random_state=42,
    )

    cv_results = cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)
    print("\n      Cross-validation results:")
    print(f"      - Mean RMSE: {cv_results['test_rmse'].mean():.4f}")
    print(f"      - Mean MAE:  {cv_results['test_mae'].mean():.4f}")

    # ----------------------------------------------------------------------
    # Step 3: Train on full dataset
    # ----------------------------------------------------------------------
    print("\n[3/4] Training on full dataset...")
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    print("      Training completed!")

    # ----------------------------------------------------------------------
    # Step 4: Save model
    # ----------------------------------------------------------------------
    print(f"\n[4/4] Saving model to {model_path}...")
    with open(model_path, "wb") as f:
        pickle.dump(algo, f)
    print("      Model saved successfully!")

    # ----------------------------------------------------------------------
    # Test prediction
    # ----------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Testing the model...")
    print("=" * 60)

    test_user = "196"
    test_movie = "242"
    prediction = algo.predict(test_user, test_movie)

    print("\nSample prediction:")
    print(f"  User ID:           {test_user}")
    print(f"  Movie ID:          {test_movie}")
    print(f"  Predicted Rating:  {prediction.est:.2f}")

    print("\n" + "=" * 60)
    print("Training complete! You can now run the API.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Start the API: uvicorn app.main:app --reload")
    print("  2. Open docs:     http://localhost:8000/docs")
    print("  3. Test predict:  POST /predict with user_id and movie_id")


if __name__ == "__main__":
    main()
