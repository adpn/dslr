import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

training_data = pd.read_csv('datasets/dataset_train.csv')
training_data = training_data.drop(columns=['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand'])
training_data = training_data.dropna()

label_encoder = LabelEncoder()
training_data['Hogwarts House'] = label_encoder.fit_transform(training_data['Hogwarts House'])
X_train = training_data.drop(columns=['Hogwarts House'])
y_train = training_data['Hogwarts House']

model = LogisticRegression(solver='saga', max_iter=5000)
model.fit(X_train, y_train)

test_data = pd.read_csv('datasets/dataset_test.csv')
test_data = test_data.drop(columns=['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand', 'Hogwarts House'])
test_data = test_data.dropna()
predictions = model.predict(test_data)
house_names = label_encoder.inverse_transform(predictions)

output_df = pd.DataFrame({
    'Index': test_data.index,
    'Predicted Hogwarts House': house_names
})

true_labels_df = pd.read_csv('houses.csv')

merged_df = pd.merge(output_df, true_labels_df, on='Index', how='inner', suffixes=('_pred', '_true'))

y_pred = merged_df['Predicted Hogwarts House']
y_true = merged_df['Hogwarts House']

accuracy = accuracy_score(y_true, y_pred)

print(f"Accuracy: {accuracy:.2f}")