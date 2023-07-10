from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import CustomUser

@registry.register_document
class CustomUserDocument(Document):
    first_name = fields.TextField(
        attr='first_name',
        fields={
         'raw': fields.TextField(),
         'suggest': fields.CompletionField(),
     }
    )
    last_name = fields.TextField(
        attr='last_name',
        fields={
         'raw': fields.TextField(),
         'suggest': fields.CompletionField(),
     }
        )
    
    class Index:
        name = 'users'  

    class Django:
        model = CustomUser 