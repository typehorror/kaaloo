
from south.db import db
from django.db import models
from profile.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding ManyToManyField 'Profile.contacts'
        db.create_table('profile_profile_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_profile', models.ForeignKey(Profile, null=False)),
            ('to_profile', models.ForeignKey(Profile, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Dropping ManyToManyField 'Profile.contacts'
        db.delete_table('profile_profile_contacts')
        
    
    
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
            'contacts': ('models.ManyToManyField', ["'self'"], {'symmetrical': 'True', 'blank': 'True'}),
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
