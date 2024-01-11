from passlib.context import CryptContext
from datetime import datetime
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_time():
    return datetime.now()


# TODO: I will Create a new Hash Algorithm Here.

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def random_number():
    return random.randint(1000, 9999)

def calculate_average_rating(reviews):
    if not reviews:
        return 0.0

    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews)
    return round(average_rating, 2)


def group_reviews_by_doctor(reviews):
    reviews_by_doctor = {}

    for review in reviews:
        if review.doctor_id not in reviews_by_doctor:
            reviews_by_doctor[review.doctor_id] = []

        reviews_by_doctor[review.doctor_id].append(review)

    return reviews_by_doctor


def get_symptoms_list():
    return [
        'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
        'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
        'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
        'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
        'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
        'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
        'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
        'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
        'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
        'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
        'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
        'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
        'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
        'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
        'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
        'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
        'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
        'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
        'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
        'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
        'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
        'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
        'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
        'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
        'yellow_crust_ooze'
    ]
    

def get_disease_list():
    return [
        'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ',
        'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)',
        'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
        'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
        'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
        'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo'
    ]

    
def map_disease_to_doctor(disease):
    rheumatologist = ['Osteoarthristis', 'Arthritis']
    cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']
    ent_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']
    orthopedist = []
    neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']
    allergist_immunologist = ['Allergy', 'Pneumonia', 'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']
    urologist = ['Urinary tract infection', 'Dimorphic hemmorhoids(piles)']
    dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']
    gastroenterologist = [
            'Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis', 'Hepatitis E',
            'Alcoholic hepatitis', 'Jaundice', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia'
        ]

    consultdoctor = "Medical Practitioner"
    
    if disease in rheumatologist:
        consultdoctor = "Rheumatologist"

    if disease in cardiologist:
        consultdoctor = "Cardiologist"

    elif disease in ent_specialist:
        consultdoctor = "ENT specialist"

    elif disease in orthopedist:
        consultdoctor = "Orthopedist"

    elif disease in neurologist:
        consultdoctor = "Neurologist"

    elif disease in allergist_immunologist:
        consultdoctor = "Allergist/Immunologist"

    elif disease in urologist:
        consultdoctor = "Urologist"

    elif disease in dermatologist:
        consultdoctor = "Dermatologist"

    elif disease in gastroenterologist:
        consultdoctor = "Gastroenterologist"
        
    return consultdoctor

