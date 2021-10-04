from datetime import datetime

from rest_framework.response import Response
from rest_framework import status


def validate_datetime(func):
    def search(view, request, *args, **kwargs):
        try:
            param = request.data

            if param.get("date_param") is not None:
                kwargs['param'] = {
                    'type': 'date',
                    'param': datetime.strptime(param.get("date_param"), '%Y-%m-%d')
                }
            elif param.get("datetime_param") is not None:
                kwargs['param'] = {
                    'type': 'datetime',
                    'param': datetime.strptime(param.get("datetime_param"), '%Y-%m-%d %H:%M:%S')
                }
            else:
                return Response({"error": "Please provide either date or datetime for searching"}, status=status.HTTP_400_BAD_REQUEST)
            
            return func(view, request, *args, **kwargs)
        except Exception as e:
            return Response({"error": "Invalid datetime format"}, status=status.HTTP_400_BAD_REQUEST)
    return search