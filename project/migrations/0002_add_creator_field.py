
from south.db import db
from django.db import models
from project.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Project.creator'
        db.add_column('project_project', 'creator', models.ForeignKey(orm['auth.User'], related_name='projects'))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Project.creator'
        db.delete_column('project_project', 'creator_id')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'project.project': {
            'collaborators': ('models.ManyToManyField', ['User'], {'related_name': "'projects_as_collaborator'", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'creator': ('models.ForeignKey', ['User'], {'related_name': "'projects'"}),
            'description': ('models.TextField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('models.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True'}),
            'owners': ('models.ManyToManyField', ['User'], {'related_name': "'owned_projects'"}),
            'spectators': ('models.ManyToManyField', ['User'], {'related_name': "'projects_as_spectator'", 'null': 'True', 'blank': 'True'}),
            'status': ('models.CharField', [], {'default': "'active'", 'max_length': '10'}),
            'title': ('models.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['project']
