from app import app
from flask import render_template, request, jsonify
import pickle
from sklearn.preprocessing import StandardScaler
import os

# Load the trained description_model and vectorizers

base_path = os.path.dirname(__file__)

description_model = pickle.load(open(os.path.join(base_path, 'pkl', 'description_model.pkl'), 'rb'))
count_vect = pickle.load(open(os.path.join(base_path, 'pkl', 'count_vect.pkl'), 'rb'))
tfidf_transformer = pickle.load(open(os.path.join(base_path, 'pkl', 'tfidf.pkl'), 'rb'))
priority_model = pickle.load(open(os.path.join(base_path, 'pkl', 'priority_model.pkl'), 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        ticket_description = request.form['ticket_description']
        contact_type = request.form['contact_type']
        category = float(request.form['category'])
        subcategory = float(request.form['subcategory'])
        impact = request.form['impact']
        notify = request.form['notify']
        
        # Preprocessing

        # 1, For Department
        test_count = count_vect.transform([ticket_description])
        test_tfidf = tfidf_transformer.transform(test_count)

        # 2, For Priority

        # contact type encoding mapping
        map1= {'direct_opening': 0, 'email': 1, 'ivr': 2, 'phone': 3, 'self_service': 4}
        # impact encoding mapping
        map2={'high': 0, 'medium': 1, 'low': 2}
        # notify encoding mapping
        map3 = {'no': 0, 'yes': 1}

        input_vector=[[map1[contact_type],category,subcategory,map2[impact],map3[notify]]]

        sc = StandardScaler()
        input_vector = sc.fit_transform(input_vector)
        

      

        # Prediction
    
        # Make prediction using the description_model
        prediction1 = description_model.predict(test_tfidf)

        # Make prediction using the priority Model
        prediction2 = priority_model.predict(input_vector)


        topic_mapping1 = {
            0: 'Bank Account services',
            1: 'Credit card or prepaid card',
            2: 'Others',
            3: 'Theft/Dispute Reporting',
            4: 'Mortgage/Loan'
        }
        topic_mapping2 = {
            0: 'Critical',
            1: 'High',
            2: 'Moderate',
            3: 'Low',
            4: 'Low'
        }
        
        answer1 = topic_mapping1[prediction1[0]]
        answer2 = topic_mapping2[prediction2[0]]
        
     
     # Redirect to the new page with prediction data
        return render_template('index2.html', prediction1=answer1,prediction2=answer2)
