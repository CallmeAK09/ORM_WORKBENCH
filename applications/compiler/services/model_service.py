from django.db import models, connection

from applications.compiler.services.serializer import get_field_name, get_record_dict
from applications.compiler.models import Author, Book, Library


def inject_app_label(code):
    lines = code.split('\n')
    new_lines = []
    is_inside = False
    indent = ""

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith("class") and "models.Model" in stripped_line:
            is_inside = True
            indent = line[ : len(line) - len(line.lstrip())] + "    "
            new_lines.append(line)
            continue
        
        if is_inside and stripped_line.startswith("class Meta"):
            is_inside = False
            new_lines.append(line)
            continue

        if is_inside and (stripped_line.startswith("class") or stripped_line == ""):
            new_lines.append(indent + "class Meta:")
            new_lines.append(indent + "    app_label = 'compiler'")
            is_inside = False
        
        new_lines.append(line)

    if is_inside:
        new_lines.append(indent + "class Meta:")
        new_lines.append(indent + "    app_label = 'compiler'")
    
    return "\n" . join(new_lines)


def get_tables_data(env=None):
    tables_data = []
    
    for model in [Author, Book, Library]:
        instances = (
            model.objects.select_related()
            .prefetch_related(*[f.name for f in model._meta.many_to_many])
            .all()[:10]
        )

        tables_data.append({
            'name':model.__name__,
            'fields':get_field_name(model),
            'records':[get_record_dict(inst, model) for inst in instances]
        })

    if env:
        for name, obj in env.items():
            if obj in [Author, Book, Library]:
                continue
            if isinstance(obj, type) and issubclass(obj, models.Model) and obj is not models.Model:
                
                table_name = obj._meta.db_table

                if table_name not in connection.introspection.table_names():
                    with connection.schema_editor() as schema_editor:
                        schema_editor.create_model(obj)

                        try:
                            obj.objects.create()
                        except Exception:
                            pass

                else:
                    with connection.cursor() as cursor:
                        description = connection.introspection.get_table_description(cursor, table_name)
                        existing_columns = {col.name for col in description}

                    for field in obj._meta.fields:
                        if field.column not in existing_columns:
                            with connection.schema_editor() as schema_editor:
                                try:
                                    schema_editor.add_field(obj, field)
                                except Exception:
                                    pass
                
                try:
                    instances = (
                        obj.objects.select_related()
                        .prefetch_related(*[f.name for f in obj._meta.many_to_many])
                        .all()[:10]
                    )

                    records = [get_record_dict(inst, obj) for inst in instances]
                except Exception:
                    records = []
                
                tables_data.append({
                    'name':name + '(Custom)',
                    'fields':get_field_name(obj),
                    'records':records
                })
    
    return tables_data