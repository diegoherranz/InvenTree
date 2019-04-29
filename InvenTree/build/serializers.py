"""
JSON serializers for Build API
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from InvenTree.serializers import InvenTreeModelSerializer

from .models import Build, BuildItem

class BuildSerializer(InvenTreeModelSerializer):
    """ Serializes a Build object """

    url = serializers.CharField(source='get_absolute_url', read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Build
        fields = [
            'pk',
            'url',
            'title',
            'creation_date',
            'completion_date',
            'part',
            'quantity',
            'status',
            'status_text',
            'notes']


class BuildItemSerializer(InvenTreeModelSerializer):
    """ Serializes a BuildItem object """

    part = serializers.CharField(source='stock_item.part', read_only=True)

    class Meta:
        model = BuildItem
        fields = [
            'build',
            'part',
            'stock_item',
            'quantity'
        ]
