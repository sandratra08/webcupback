import os
import random
import spacy

from fastapi import APIRouter, Depends, HTTPException, status
from googletrans import Translator
from tortoise import Tortoise
from project.router.user.user import connected_user
from project.schemas.dream.dream import InputData
from project.schemas.user.user import UserDB
from project.utils.keywords import *
from fastapi.security.oauth2 import OAuth2PasswordBearer
from tortoise.contrib.pydantic import pydantic_model_creator

from project.models import Dream, User

# Load the SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

router = APIRouter()
Tortoise.init_models(["project.models"], "models")
pydantyc_model = pydantic_model_creator(Dream)

@router.get("/")
async def get_description(user: UserDB = Depends(connected_user), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    if token is not None:
        return await pydantyc_model.from_queryset_single(Dream.get(user_id=user.id))


@router.post("/")
async def classify_input_text(input_data: InputData, user: UserDB = Depends(connected_user), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    if token is not None:
        description = input_data.description

        # Translate the input text to English
        translator = Translator()
        english_text = translator.translate(
            description, src='auto', dest='en').text

        doc = nlp(english_text)

        romantic_score = sum(
            1 for token in doc if token.lower_ in romantic_keywords)
        work_score = sum(1 for token in doc if token.lower_ in work_keywords)
        academic_score = sum(
            1 for token in doc if token.lower_ in academic_keywords)
        disease_score = sum(
            1 for token in doc if token.lower_ in disease_keywords)
        nightmare_score = sum(
            1 for token in doc if token.lower_ in nightmare_keywords)

        if romantic_score > work_score and romantic_score > academic_score and romantic_score > disease_score and romantic_score > nightmare_score:
            classification = "romantic encounter"
            response_template = "It sounds like you're focused on matters of the heart. In the future, you might {} and feel {} about your relationship. Remember to {} and {} to keep your love alive."
            response = nlp(response_template.format(
                random.choice(["experience", "encounter", "face"]),
                random.choice(["happy", "fulfilled", "satisfied"]),
                random.choice(["communicate", "listen", "compromise"]),
                random.choice(
                    ["be patient", "show empathy", "forgive yourself"])
            )).text
        elif work_score > romantic_score and work_score > academic_score and work_score > disease_score and work_score > nightmare_score:
            classification = "problems with colleagues at work"
            response_template = "It sounds like you're having some issues with your colleagues at work. In the future, you might {} and try to {} the situation. Remember to {} and {} to maintain a healthy work environment."
            response = nlp(response_template.format(
                random.choice(["encounter", "experience", "face"]),
                random.choice(["communicate", "negotiate", "collaborate"]),
                random.choice(["stay calm", "be patient", "take a break"]),
                random.choice(
                    ["show empathy", "be respectful", "forgive yourself"])
            )).text
        elif academic_score > romantic_score and academic_score > work_score and academic_score > disease_score and academic_score > nightmare_score:
            classification = "academic difficulty"
            response_template = "It sounds like you're experiencing some difficulties with your studies. In the future, you might {} and seek {} to improve your academic performance. Remember to {} and {} to stay motivated and achieve your goals."
            response = nlp(response_template.format(
                random.choice(["study more", "seek help", "review"]),
                random.choice(["stay organized", "set goals", "manage time"]),
                random.choice(["ask questions", "participate", "persevere"]),
                random.choice(
                    ["stay positive", "believe in yourself", "celebrate progress"])
            )).text
        elif disease_score > romantic_score and disease_score > work_score and disease_score > academic_score and disease_score > nightmare_score:
            classification = "serious diseases"
            response_template = "It sounds like you're going through a tough time with your health. In the future, you might {} and seek {} to manage your condition. Remember to {} and {} to take care of yourself."
            response = nlp(response_template.format(
                random.choice(
                    ["seek medical advice", "monitor your symptoms", "get treatment"]),
                random.choice(
                    ["stay informed", "reach out for support", "manage stress"]),
                random.choice(["maintain a healthy lifestyle",
                               "take medication as prescribed", "attend medical appointments"]),
                random.choice(
                    ["be patient", "stay hopeful", "focus on self-care"])
            )).text
        elif nightmare_score > romantic_score and nightmare_score > work_score and nightmare_score > academic_score and nightmare_score > disease_score:
            classification = "nightmare"
            response = "Go to a specialist"
        else:
            classification = "Unknown"
            response = "Would you mind to add more specifications on your description?"

        await Dream.create(
            description=input_data.description,
            prediction=translator.translate(
                classification, src="en", dest="fr").text,
            advice=translator.translate(response, src="en", dest="fr").text,
            user_id=user.id
        )

        return {
            "prediction": classification,
            "prediction_fr": translator.translate(classification, src="en", dest="fr").text,
            "response": response,
            "response_fr": translator.translate(response, src="en", dest="fr").text
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentification requise",
        )
