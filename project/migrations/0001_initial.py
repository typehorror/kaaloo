
from south.db import db
from django.db import models
from project.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Project'
        db.create_table('project_project', (
            ('status', models.CharField(default='active', max_length=10)),
            ('description', models.TextField(blank=True)),
            ('modification_date', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ('title', models.CharField(max_length=50)),
            ('creation_date', models.DateTimeField(auto_now_add=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('project', ['Project'])
        
        # Adding ManyToManyField 'Project.owners'
        db.create_table('project_project_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(Project, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
        # Adding ManyToManyField 'Project.collaborators'
        db.create_table('project_project_collaborators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(Project, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
        # Adding ManyToManyField 'Project.spectators'
        db.create_table('project_project_spectators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(Project, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Project'
        db.delete_table('project_project')
        
        # Dropping ManyToManyField 'Project.owners'
        db.delete_table('project_project_owners')
        
        # Dropping ManyToManyField 'Project.collaborators'
        db.delete_table('project_project_collaborators')
        
        # Dropping ManyToManyField 'Project.spectators'
        db.delete_table('project_project_spectators')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'project.project': {
            'collaborators': ('models.ManyToManyField', ['User'], {'related_name': "'projects_as_collaborator'", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
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
