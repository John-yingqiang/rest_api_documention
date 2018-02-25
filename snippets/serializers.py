# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Snippet,LANGUAGE_CHOICES,STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	code = serializers.CharField(style={'base_template':'textarea.html'})
	linenos = serializers.BooleanField(required=False)
	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

	def create(self, validated_data):
		"""
		create and return a new 'Snippet' instance, given the validated data
		"""
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing 'Snippet' instance, given the validated data
		"""
		instance.title = validated_data.get('title', instance.title)
		instance.code = validated_data.get('code', instance.code)
		instance.linenos = validated_data.get('linenos', instance.linenos)
		instance.language = validated_data.get('language', instance.language)
		instance.style = validated_data.get('style', instance.style)
		instance.save()
		return instance

class SnippetModelSerializerNoHyperlinked(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Snippet
		fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')

class UserSerializerModel(serializers.ModelSerializer):
	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
# 因为'snippets'在用户模型中是一个相反的关系，默认情况下在使用ModelSerializer类时我们不会包括，所以我们需要手动为用户序列添加这个字段
	class Meta:
		model = User
		fields = ('id', 'username', 'snippets')
#    以下是HyperlinkedModelSerializer不同于ModelSerializer的地方：
#    HyperlinkedModelSerializer默认不包括pk字段。
#    它只包括一个url字段，使用HyperlinkedIndentityField。
#    关系使用HyperlinkedRelatedField，而不是PrimaryKeyRelatedField。 我们能使用超链接快速重写现存的序列。在snippets/serializers.py中添加：

class SnippetModelSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

	class Meta:
		model = Snippet
		fields = ('url', 'highlight', 'owner',
				  'title', 'code', 'linenos', 'language', 'style')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'username', 'snippets')

































