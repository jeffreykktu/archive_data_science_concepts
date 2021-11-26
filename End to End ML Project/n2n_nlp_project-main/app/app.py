# Core packages
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# Utils
import joblib


# load the pipeline
model_path = "models/20210722_emotion_classifier_pipe_lr_best.pkl"
pipe_lr = joblib.load(open(model_path, "rb"))

# Create Functions
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    # Return a string
    return results[0] 

def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    # Return the entire dictionary
    return results

emotion_emoji_dict = {
    "anger": "Anger 😡",
    "disgust": "Disgust 🤢",
    "fear": "Fear 😱",
    "happy": "Happy 😆",
    "joy": "Joy 🤣",
    "neutral": "Neutral 😐",
    "sadness": "Sadness 😔",
    "shame": "Shame 😵",
    "surprise": "Surprise 😳"
    }

def main():
    st.title("Emotion Classifier")
    menu = ['Home', 'Monitor', 'About']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home - Emotion in Text")

        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area("Enter Your Text Here")
            submit_text = st.form_submit_button(label='Submit')

            if submit_text:
                col1, col2 = st.beta_columns(2)

                # Apply functions here
                prediction = predict_emotions(raw_text)
                probability = get_prediction_proba(raw_text)

                with col1:
                    st.success("Original Text")
                    st.write(raw_text)

                    st.success("Prediction")
                    st.write(emotion_emoji_dict[prediction])
                    st.write(f"Confidence Level: {np.max(probability):.3%}")
        
                with col2:
                    st.success("Prediction Probability")
                    # st.write(probability)
                    df_proba = pd.DataFrame(probability, columns=pipe_lr.classes_)
                    
                    # Print out a probability table
                    df_proba_trans = df_proba.T
                    df_proba_trans.columns = ["Probability"]
                    st.write(df_proba_trans)

                    # Transpose it so it is a vertical column
                    df_proba_clean = df_proba.T.reset_index()
                    df_proba_clean.columns = ["Emotion", "Probability"]

                    fig = alt.Chart(df_proba_clean).mark_bar().encode(x="Emotion", y="Probability", color='Emotion')
                    st.altair_chart(fig, use_container_width=True)

    elif choice == "Monitor":
        st.subheader("Monitor App")
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()