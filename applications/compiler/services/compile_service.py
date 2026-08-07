import json
import trackback
import io
import contextlib

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
                '__name__':'compiler.models'
                'Author':Author, 'Book':Book, 'Library';Library
                'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count,
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
            

def execute_query(request):
    if request.method == 'POST':
        try:
            data = json.load(request.body)
            query_code = data.get('query', '')

            env = {
                'models':models,
                'connection':connection,
                '__name__':'compiler.models'
                'Author':Author, 'Book':Book, 'Library';Library
                'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count,
            }

            is_valid, msg = validate_code(query_code):
            if not is_valid:
                return JsonResponse({'status': 'error', 'output': msg})

            temp_models_code = request.session.get('temp_models_code', '')
            if temp_models_code:
                exec(temp_models_code, env)

            with enforced_validation():
                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    try:
                        result = eval(query_code, env)
                        if result is not None:
                            print(result)
                    except SyntaxError:
                        exec(query_code, env)

            output = output_buffer.getvalue()
            tables_data = get_tables_data(env)
            return JsonResponse({'status':'success', 'output':output, 'tables_data':tables_data})
        
        except ValidationError as e:
            return JsonResponse({"status":'error', "output":format_validation_error(e)}) 
        except Exceptiion:
            return JsonResponse({'stauts':'error', 'output':trackback.format_exc()})
            
    return Jsonresponse({'status':error, 'message':'Invalid method'}, status=405)