import json
import traceback
import io
import ast
import contextlib

from django.db import models, connection
from django.http import JsonResponse
from django.db.models import Avg, Sum, Min, Max, Count, F, Q, Case, When, Value, Subquery, OuterRef, ExpressionWrapper, Exists
from django.core.exceptions import ValidationError

from .database import drop_temp_tables, reset_default_tables
from .model_service import get_tables_data, inject_app_label
from applications.compiler.models import Author, Book, Library
from applications.compiler.sandbox.validator import validate_code, format_validation_error
from applications.compiler.sandbox.executor import enforce_validation

def clear_custom_models():
    from django.apps import apps
    default_models = {'author', 'book', 'library'}
    app_models = apps.all_models.get('compiler', {})
    for model_name in list(app_models.keys()):
        if model_name not in default_models:
            app_models.pop(model_name, None)



def save_model_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            models_code = inject_app_label(data.get('models_code', ''))

            is_valid, msg = validate_code(models_code)
            if not is_valid:
                return JsonResponse({'status':'error', 'output':msg})

            old_code = request.session.get('temp_models_code', '')
            if models_code != old_code:
                drop_temp_tables()

            request.session['temp_models_code'] = models_code
            request.session.modified = True

            env = {
                'models':models,
                'connection':connection,
                '__name__':'applications.compiler.models',
                'Author':Author, 'Book':Book, 'Library':Library,
                'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count, 'F':F, 'Q':Q,
                'Case':Case, 'When':When, 'Value':Value, 'Subquery':Subquery, 'OuterRef':OuterRef, 'ExpressionWrapper':ExpressionWrapper, 'Exists':Exists
            }

            clear_custom_models()
            with enforce_validation():
                exec(models_code, env)

            tables_data = get_tables_data(env)

            return JsonResponse({
                'status':'success',
                'message':'Models saved successfully.',
                'tables_data':tables_data
            })

        except ValidationError as e:
            return JsonResponse({"status":'error', "output":format_validation_error(e)}) 
        except Exception:
            return JsonResponse({'status':'error', 'output':traceback.format_exc()})
            

def execute_query_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query_code = data.get('query', '')

            env = {
                'models':models,
                'connection':connection,
                '__name__':'applications.compiler.models',
                'Author':Author, 'Book':Book, 'Library':Library,
                'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count, 'F':F, 'Q':Q,
                'Case':Case, 'When':When, 'Value':Value, 'Subquery':Subquery, 'OuterRef':OuterRef, 'ExpressionWrapper':ExpressionWrapper, 'Exists':Exists
            }

            is_valid, msg = validate_code(query_code)
            if not is_valid:
                return JsonResponse({'status': 'error', 'output': msg})

            clear_custom_models()

            temp_models_code = request.session.get('temp_models_code', '')
            if temp_models_code:
                exec(temp_models_code, env)
                get_tables_data(env)

            # Pre-compile any custom models defined directly in the query to ensure their tables exist
            try:
                tree = ast.parse(query_code)
                class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
                if class_nodes:
                    new_tree = ast.Module(body=class_nodes, type_ignores=[])
                    exec(compile(new_tree, filename="<string>", mode="exec"), env)
                    get_tables_data(env)
            except Exception:
                pass

            # Force debug cursor to capture SQL queries
            connection.force_debug_cursor = True
            connection.queries_log.clear()

            with enforce_validation():
                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    try:
                        result = eval(query_code, env)
                        if result is not None:
                            # Evaluate QuerySet or raw query generators to ensure queries run and print result
                            if hasattr(result, '_fetch_all'):
                                list(result)
                            print(result)
                    except SyntaxError:
                        exec(query_code, env)

            output = output_buffer.getvalue()
            
            # Format and append generated SQL queries
            sql_queries = []
            for q in connection.queries:
                sql = q.get('sql')
                if sql:
                    sql_queries.append(sql)
            
            if sql_queries:
                output += "\n\n--- Generated SQL ---"
                for idx, sql in enumerate(sql_queries, 1):
                    output += f"\nQuery {idx}:\n{sql}\n"

            tables_data = get_tables_data(env)
            return JsonResponse({'status':'success', 'output':output, 'tables_data':tables_data})
        
        except ValidationError as e:
            return JsonResponse({"status":'error', "output":format_validation_error(e)}) 
        except Exception:
            return JsonResponse({'status':'error', 'output':traceback.format_exc()})
            
    return JsonResponse({'status':'error', 'message':'Invalid method'}, status=405)


def reset_session_service(request):
    drop_temp_tables()
    reset_default_tables()
    request.session.flush()
    request.session.create()
    request.session['db_initialized'] = True

def build_context_service(request):
    if not request.session.get('db_initialized', False):
        reset_default_tables()
        request.session['db_initialized'] = True

    env = None
    temp_models_code = request.session.get('temp_models_code', '')
    if temp_models_code:
        suffix = get_session_suffix(request)
        temp_models_code = inject_app_label(temp_models_code, suffix)

    if temp_models_code:
        clear_custom_models()
        env = {
            'models':models,
            'connection':connection,
            '__name__':'applications.compiler.models',
            'Author':Author, 'Book':Book, 'Library':Library,
            'Avg':Avg, 'Sum':Sum, 'Min':Min, 'Max':Max, 'Count':Count, 'F':F, 'Q':Q,
            'Case':Case, 'When':When, 'Value':Value, 'Subquery':Subquery, 'OuterRef':OuterRef, 'ExpressionWrapper':ExpressionWrapper, 'Exists':Exists
        }

        try:
            exec(temp_models_code, env)
        except Exception:
            pass

    tables_data = get_tables_data(env)

    context = {
        'tables_data':tables_data,
        'temp_models_code':temp_models_code
    }
    return context

