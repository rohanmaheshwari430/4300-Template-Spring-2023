import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app with credentials
cred = credentials.Certificate('backend/firebase/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Example 2D numpy arraycl
data = np.load('backend/cossim_matrix.npy')

# Write each value to Firebase
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        doc_ref = db.collection('cosine_similarity').document(f'{i}').collection('scores').document(int(data[i][j]))
        print(data[i][j])
        doc_ref.set({'value': str(data[i][j])})

print('Data written to Firebase')
