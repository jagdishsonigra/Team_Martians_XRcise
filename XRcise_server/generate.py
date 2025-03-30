import pandas as pd

# Load the dataset
df = pd.read_csv("G:\Hack-A-Thon\COEP_2025\XRcise_server\data\hello.csv")

# Step 1: Remove duplicates
df.drop_duplicates(inplace=True)

# Step 2: Handle missing values
# Check for missing values
print("Missing values:\n", df.isnull().sum())

# Fill missing values or drop rows (example: drop rows with any missing values)
df.dropna(inplace=True)

# Step 3: Standardize categorical values
# Example: Standardizing Agegroup
df['Agegroup'] = df['Agegroup'].replace({
    "Jan-18": "January 2018",
    "30-50": "30-50 years",
    "50+": "50 years and above"
})

# Step 4: Check for typos and standardize
# Example: Standardizing Exercise Recommendations
df['Exerciserecommendation'] = df['Exerciserecommendation'].str.strip().str.lower()
df['Exerciserecommendation'] = df['Exerciserecommendation'].replace({
    "jumping jacks": "Jumping Jacks",
    "squat exercise": "Squat Exercise",
    "shoulder abduction": "Shoulder Abduction",
    "knee flexion": "Knee Flexion",
    "hip flexion": "Hip Flexion"
})

# Step 5: Balance classes (if necessary)
# Check class distribution
print("Class distribution:\n", df['Exerciserecommendation'].value_counts())

# If classes are imbalanced, consider oversampling or undersampling techniques

# Step 6: Save the cleaned dataset
df.to_csv("G:\Hack-A-Thon\COEP_2025\XRcise_server\data\cleaned_hello.csv", index=False)

print("Dataset cleaned and saved as cleaned_hello.csv")