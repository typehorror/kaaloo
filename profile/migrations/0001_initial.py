
from south.db import db
from django.db import models
from profile.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Registration'
        db.create_table('profile_registration', (
            ('creation_date', models.DateTimeField(auto_now_add=True)),
            ('id', models.AutoField(primary_key=True)),
            ('key', models.CharField(default=get_uuid, unique=True, max_length=55, db_index=True)),
            ('email', models.EmailField()),
        ))
        db.send_create_signal('profile', ['Registration'])
        
        # Adding model 'Profile'
        db.create_table('profile_profile', (
            ('city', models.CharField(max_length=50, blank=True)),
            ('address1', models.CharField(max_length=255, blank=True)),
            ('address2', models.CharField(max_length=255, blank=True)),
            ('sex', models.CharField("Gender", blank=True, max_length=6)),
            ('phone', models.CharField(max_length=20, blank=True)),
            ('state', models.CharField(blank=True, max_length=3)),
            ('date_of_birth', models.DateField(null=True, blank=True)),
            ('user', models.ForeignKey(orm['auth.User'], related_name='profile', unique=True)),
            ('cellular', models.CharField(max_length=20, blank=True)),
            ('country', models.CharField(blank=True, max_length=4)),
            ('id', models.AutoField(primary_key=True)),
            ('zip_code', models.CharField(max_length=10, blank=True)),
        ))
        db.send_create_signal('profile', ['Profile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Registration'
        db.delete_table('profile_registration')
        
        # Deleting model 'Profile'
        db.delete_table('profile_profile')
        
    
    
    models = {
        'profile.registration': {
            'creation_date': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'email': ('models.EmailField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'key': ('models.CharField', [], {'default': 'get_uuid', 'unique': 'True', 'max_length': '55', 'db_index': 'True'})
        },
        'profile.profile': {
            'address1': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cellular': ('models.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'city': ('models.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('models.CharField', [], {'blank': 'True', 'max_length': '4'}),
            'date_of_birth': ('models.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'phone': ('models.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'sex': ('models.CharField', ['"Gender"'], {'blank': 'True', 'max_length': '6'}),
            'state': ('models.CharField', [], {'blank': 'True', 'max_length': '3'}),
            'user': ('models.ForeignKey', ['User'], {'related_name': "'profile'", 'unique': 'True'}),
            'zip_code': ('models.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['profile']
