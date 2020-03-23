# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.skill_builder import CustomSkillBuilder
from alexa.util import *
import logging
import ask_sdk_core.utils as ask_utils
import os
import json
import locale
import requests
import calendar
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = welcomeMessage
        reprompt = welcomeReprompt
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "INITIALIZING"

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class CaptureArtistIntentHandler(AbstractRequestHandler):
    """Handler for Capturing the Favorite Artist."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CaptureArtistIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        attr = handler_input.attributes_manager.session_attributes

        artist = slots["artistName"].value
        attr["artist"] = artist

        speak_output = capturedArtist(artist) + " " + startQuiz(artist)
        reprompt = welcomeReprompt

        return (handler_input.response_builder.speak(speak_output).ask(
            reprompt).response)


class StartQuizIntentHandler(AbstractRequestHandler):
    """Handler for Starting the Quiz."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StartQuizIntent")(handler_input) or is_intent_name("AMAZON.StartoverIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Handle premature "Start Quiz"
        attr = handler_input.attributes_manager.session_attributes

        if "artist" in attr:
            # Set State to "In Quiz"
            attr["state"] = "QUIZ"
            attr["score"] = ""
            attr["questionNumber"] = 1
            questionNumber = attr["questionNumber"]
            artistName = attr["artist"]
            attr["questionSet"] = getQuestionSet(artistName)
            questionSet = attr["questionSet"]
            speak_output = getQuestion(questionSet, questionNumber)
            reprompt = questionHelp(artistName, questionNumber)

            return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)

        else:
            speak_output = helpWithArtistMessage

            return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)


class QuizAnswerHandler(AbstractRequestHandler):
    """Handler for Answers to the Quiz."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AnswerIntent")(handler_input) and attr.get("state") == "QUIZ")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Handle "score"
        slots = handler_input.request_envelope.request.intent.slots
        attr = handler_input.attributes_manager.session_attributes

        attr["questionNumber"] += 1
        artistName = attr["artist"]
        questionNumber = attr["questionNumber"]
        score = attr["score"]
        attr["score"] = getScore(score, slots)

        if questionNumber < 4:
            speak_output = getQuestion(artistName, questionNumber)
            reprompt = questionHelp(artistName, questionNumber)

            return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)

        else:
            score = attr["score"]
            attr['song'] = getFinalResponse(artistName, score)
            song = attr['song']
            speak_output = song

            return (handler_input.response_builder.speak(speak_output).ask(exitMessage).response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        attr = handler_input.attributes_manager.session_attributes
        if attr["state"] == "INITIALIZING":
            if "artist" in attr:
                artist = attr["artist"]
                speak_output = helpWithQuizMessage(artist)
            else:
                speak_output = helpWithArtistMessage
        else:
            if "song" in attr:
                song = attr["song"]
                artist = attr["artist"]
                speak_output = repeatFinal(artist, song)
            else:
                question = attr["questionNumber"]
                artist = attr["artist"]
                speak_output = questionHelp(artist, question)

        return (handler_input.response_builder.speak(speak_output).ask(
            errorMessage).response)


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
                or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = goodbyeMessage

        return (handler_input.response_builder.speak(speak_output).response)


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """The fallback intent handles all "Unknown" requests."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speak_output = fallbackErrorMessage

        return (handler_input.response_builder.speak(speak_output).response)


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        attr = handler_input.attributes_manager.session_attributes
        if attr["state"] == "INITIALIZING":
            if "artist" in attr:
                artist = attr["artist"]
                speak_output = helpWithQuizMessage(artist)
            else:
                speak_output = helpWithArtistMessage
        else:
            if "song" in attr:
                song = attr["song"]
                artist = attr["artist"]
                speak_output = repeatFinal(artist, song)
            else:
                question = attr["questionNumber"]
                artist = attr["artist"]
                speak_output = questionHelp(artist, question)

        return (handler_input.response_builder.speak(speak_output).ask(
            errorMessage).response)


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureArtistIntentHandler())
sb.add_request_handler(StartQuizIntentHandler())
sb.add_request_handler(QuizAnswerHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())


sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
