from app import app
from flask import render_template, request, jsonify
import pickle

# Load the trained model and vectorizers
model = pickle.load(open('/workspaces/ticket_priority_resolution_time_predictor/myflaskproject/app/pkl/grid_search_log.pkl', 'rb'))
count_vect = pickle.load(open('/workspaces/ticket_priority_resolution_time_predictor/myflaskproject/app/pkl/count_vect.pkl', 'rb'))
tfidf_transformer = pickle.load(open('/workspaces/ticket_priority_resolution_time_predictor/myflaskproject/app/pkl/tfidf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        ticket_description = request.form['ticket_description']
        
        # Preprocess the input
        test_count = count_vect.transform([ticket_description])
        test_tfidf = tfidf_transformer.transform(test_count)
        
        # Make prediction using the model
        prediction = model.predict(test_tfidf)

        topic_mapping = {
            0: 'Bank Account services',
            1: 'Credit card or prepaid card',
            2: 'Others',
            3: 'Theft/Dispute Reporting',
            4: 'Mortgage/Loan'
        }
        
        answer = topic_mapping[prediction[0]]
        
        # Return the result to the user
        return jsonify({'prediction': answer})
