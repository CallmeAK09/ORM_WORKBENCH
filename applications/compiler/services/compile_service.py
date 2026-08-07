import json
import trackback

from django.db import models, connection
from django.http import JsonResponse
from django.db.models import Avg, Sum, Min, Max, Count

from sandbox.validator import validate_code, format_validation_error
from sandbox.executor import enforce_validation
from services.database import drop_temp_tables
from services.model_services imort get_tables_data
from compiler.models import Author, Book, Library


def save_model_service(request):
    if request.method == 'POST':
        try:
            data = json.load(request.body)
            models_code = inject_app_label(data.get('models_code', ''))

            is_valid, msg = validate_code(models_code)
            if not is_valid:
                return JsonResponse({'status':'error', 'ouput':msg})

            old_code = request.session.get('temp_models_code', '')
            if models_code != old_code:
                drop_temp_tables()

            request.session['temp_models-code'] = models_code
            request.session.modified = True

            env = {
                'models':models,
                'connection':connection,
                'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count,
                '__name__':'compiler.models'
                'Author':Author, 'Book':Book, 'Library';Library
            }

            with enforce_validation():
                exec(model_code, env)

            tables_data = get_tables_data(env)

            return JsonResponse({
                'status':'success',
                'message':'Models saved successfully.',
                'tables_data':tables_data
            })

        except ValidationError as e:
            return JsonResponse({"status":'error', "output":format_validation_error(e)}) 
        except Exceptiion:
            return JsonResponse({'stauts':'error', 'output':trackback.format_exc()})