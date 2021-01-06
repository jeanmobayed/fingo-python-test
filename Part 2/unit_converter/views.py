from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import logging
import json

from unit_converter.modules.input_parser import InputParser

logger = logging.getLogger(__name__)

def home(request):
	return render(request, 'unit_converter/home.html')

@csrf_exempt
@require_http_methods(["POST"])
def process_input(request):
    DEFAULT_ANSWER = "I have no idea what you are talking about"

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    input_array = body["input"].splitlines() 
    #logger.error(input_array)

    parser = InputParser(DEFAULT_ANSWER)

    info = parser.clasify_input(input_array)
    error_msgs = info['error_msgs']

    logger.error(info)


    if len(info['ref_words']) > 0:
        result = parser.process_info(info['ref_words'], info['price_msgs'])
    
        if result:
            error_msgs.extend(result)

        answers = parser.answer_questions(info['questions'])

        answers.extend(error_msgs)

        prices = parser.get_price_book()
        word = parser.get_words_book()

        logger.error(word)
        logger.error(prices)

        return JsonResponse(answers, safe=False)

    else:
        return JsonResponse(["No correct inputs found."], safe=False)
    